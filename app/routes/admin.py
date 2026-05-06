from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Product, Order
from ..forms import ProductForm

admin_bp = Blueprint("admin", __name__)


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)
    return wrapper


@admin_bp.route("/")
@admin_required
def dashboard():
    product_count = Product.query.count()
    order_count = Order.query.count()
    return render_template("admin/dashboard.html", product_count=product_count, order_count=order_count)


@admin_bp.route("/products")
@admin_required
def products():
    items = Product.query.order_by(Product.created_at.desc()).all()
    return render_template("admin/products.html", products=items)


@admin_bp.route("/products/new", methods=["GET", "POST"])
@admin_required
def product_new():
    form = ProductForm()
    if form.validate_on_submit():
        p = Product(
            name=form.name.data,
            description=form.description.data or "",
            price=form.price.data,
            stock_quantity=form.stock_quantity.data,
            image_url=form.image_url.data or "",
            is_active=form.is_active.data,
        )
        db.session.add(p)
        db.session.commit()
        flash("Product created.", "success")
        return redirect(url_for("admin.products"))
    return render_template("admin/product_form.html", form=form, action="New product")


@admin_bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@admin_required
def product_edit(product_id: int):
    p = Product.query.get_or_404(product_id)
    form = ProductForm(obj=p)
    if form.validate_on_submit():
        p.name = form.name.data
        p.description = form.description.data or ""
        p.price = form.price.data
        p.stock_quantity = form.stock_quantity.data
        p.image_url = form.image_url.data or ""
        p.is_active = form.is_active.data
        db.session.commit()
        flash("Product updated.", "success")
        return redirect(url_for("admin.products"))
    return render_template("admin/product_form.html", form=form, action=f"Edit: {p.name}")


@admin_bp.route("/products/<int:product_id>/delete", methods=["POST"])
@admin_required
def product_delete(product_id: int):
    p = Product.query.get_or_404(product_id)
    db.session.delete(p)
    db.session.commit()
    flash("Product deleted.", "info")
    return redirect(url_for("admin.products"))


@admin_bp.route("/orders")
@admin_required
def orders():
    items = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("admin/orders.html", orders=items)


@admin_bp.route("/orders/<int:order_id>")
@admin_required
def order_detail(order_id: int):
    order = Order.query.get_or_404(order_id)
    return render_template("admin/order_detail.html", order=order)
