from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, IntegerField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional, URL


class RegisterForm(FlaskForm):
    full_name = StringField("Full name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=128)])
    confirm = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Create account")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


class CheckoutForm(FlaskForm):
    shipping_name = StringField("Full name", validators=[DataRequired(), Length(max=120)])
    shipping_address = StringField("Address", validators=[DataRequired(), Length(max=255)])
    shipping_city = StringField("City", validators=[DataRequired(), Length(max=80)])
    shipping_zip = StringField("ZIP / Postal code", validators=[DataRequired(), Length(max=20)])
    payment_method = StringField("Payment method (demo)", default="card-demo")
    submit = SubmitField("Place order")


class ProductForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=150)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=2000)])
    price = DecimalField("Price", validators=[DataRequired(), NumberRange(min=0)], places=2)
    stock_quantity = IntegerField("Stock quantity", validators=[DataRequired(), NumberRange(min=0)])
    image_url = StringField("Image URL", validators=[Optional(), URL(), Length(max=500)])
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Save product")
