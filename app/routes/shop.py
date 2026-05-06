from decimal import Decimal
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Product, Order, OrderItem
from ..forms import CheckoutForm

shop_bp = Blueprint("shop", __name__)


def _get_cart() -> dict:
    return session.get("cart", {})


def _save_cart(cart: dict) -> None:
    session["cart"] = cart
    session.modified = True


def _cart_items_with_products(cart: dict):
    items = []
    total = Decimal("0.00")
    for pid, qty in cart.items():
        product = db.session.get(Product, int(pid))
        if not product:
            continue
        line_total = Decimal(product.price) * qty
        total += line_total
        items.append({"product": product, "quantity": qty, "line_total": line_total})
    return items, total


@shop_bp.route("/products")
def products():
    page = request.args.get("page", 1, type=int)
    pagination = (
        Product.query.filter_by(is_active=True)
        .order_by(Product.created_at.desc())
        .paginate(page=page, per_page=9, error_out=False)
    )
    return render_template("shop/products.html", pagination=pagination)


@shop_bp.route("/products/<int:product_id>")
def product_detail(product_id: int):
    product = Product.query.get_or_404(product_id)
    return render_template("shop/product_detail.html", product=product)


@shop_bp.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id: int):
    product = Product.query.get_or_404(product_id)
    quantity = max(1, request.form.get("quantity", 1, type=int))
    if quantity > product.stock_quantity:
        flash("Requested quantity exceeds stock.", "warning")
        return redirect(url_for("shop.product_detail", product_id=product_id))
    cart = _get_cart()
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    _save_cart(cart)
    flash(f"Added {product.name} to cart.", "success")
    return redirect(url_for("shop.cart"))


@shop_bp.route("/cart")
def cart():
    items, total = _cart_items_with_products(_get_cart())
    return render_template("shop/cart.html", items=items, total=total)


@shop_bp.route("/cart/update/<int:product_id>", methods=["POST"])
def update_cart(product_id: int):
    quantity = request.form.get("quantity", 1, type=int)
    cart = _get_cart()
    if quantity <= 0:
        cart.pop(str(product_id), None)
    else:
        cart[str(product_id)] = quantity
    _save_cart(cart)
    return redirect(url_for("shop.cart"))


@shop_bp.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id: int):
    cart = _get_cart()
    cart.pop(str(product_id), None)
    _save_cart(cart)
    return redirect(url_for("shop.cart"))


@shop_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    items, total = _cart_items_with_products(_get_cart())
    if not items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("shop.products"))

    form = CheckoutForm()
    if form.validate_on_submit():
        for entry in items:
            if entry["quantity"] > entry["product"].stock_quantity:
                flash(f"Not enough stock for {entry['product'].name}.", "danger")
                return redirect(url_for("shop.cart"))

        order = Order(
            user_id=current_user.id,
            status="paid",
            total_amount=total,
            shipping_name=form.shipping_name.data,
            shipping_address=form.shipping_address.data,
            shipping_city=form.shipping_city.data,
            shipping_zip=form.shipping_zip.data,
        )
        db.session.add(order)
        db.session.flush()

        for entry in items:
            db.session.add(OrderItem(
                order_id=order.id,
                product_id=entry["product"].id,
                quantity=entry["quantity"],
                unit_price=entry["product"].price,
            ))
            entry["product"].stock_quantity -= entry["quantity"]

        db.session.commit()
        session.pop("cart", None)
        flash("Order placed successfully.", "success")
        return redirect(url_for("shop.order_confirmation", order_id=order.id))

    if request.method == "GET":
        form.shipping_name.data = current_user.full_name

    return render_template("shop/checkout.html", form=form, items=items, total=total)


@shop_bp.route("/orders/<int:order_id>")
@login_required
def order_confirmation(order_id: int):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash("Not authorized.", "danger")
        return redirect(url_for("main.index"))
    return render_template("shop/order_confirmation.html", order=order)
