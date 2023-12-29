from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, validators
from wtforms.validators import DataRequired, Length, EqualTo, Email
from static.market.models import User

class RegisterForm(FlaskForm):   
    def validate_username(self, username_to_check): #function name is very important here cause validate_ is searched by FlaskForm and then the object to validate
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('User with the email is already registed! Try logging')

    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])    
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')
    
class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase item')
    
class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell item')