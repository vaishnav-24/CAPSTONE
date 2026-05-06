from flask import Blueprint, render_template
from ..models import Product

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    featured = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).limit(4).all()
    return render_template("main/index.html", featured=featured)
