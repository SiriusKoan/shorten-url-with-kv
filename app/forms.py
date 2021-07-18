from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Regexp, Length, EqualTo, ValidationError


class ShortUrlForm(FlaskForm):
    old = StringField(
        "Old URL",
        validators=[
            DataRequired(),
            Regexp(
                "^(http|https):\/\/",
                message="The URL should start with https:// or http://.",
            ),
        ],
        render_kw={"placeholder": "Old URL"},
    )
    new = StringField(
        "New URL",
        validators=[
            DataRequired(),
            Regexp(
                "\w{1,10}",
                message="Bad characters in the field.",
            ),
        ],
        render_kw={"placeholder": "New URL"},
    )
    submit = SubmitField("Shorten")


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired()], render_kw={"placeholder": "Username"}
    )
    password = PasswordField(
        "Password", validators=[DataRequired()], render_kw={"placeholder": "Password"}
    )
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=4, max=30, message="The name should be 4 to 30 letters long."),
            Regexp(
                "[a-zA-Z0-9_]+",
                message="Only letters, numbers and underscore are allowed in username.",
            ),
        ],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, message="The password must contain at least 6 characters."),
        ],
        render_kw={"placeholder": "Password"},
    )
    repeat_password = PasswordField(
        "Repeat Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords not match."),
        ],
        render_kw={"placeholder": "Repeat Password"},
    )
    email = EmailField(
        "Email", validators=[DataRequired()], render_kw={"placeholder": "Email"}
    )
    submit = SubmitField("Register")


class DashboardFilterForm(FlaskForm):
    start = DateField("start", format="%Y-%m-%d", validators=[DataRequired()])
    end = DateField("end", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UserSettingForm(FlaskForm):
    password = PasswordField(
        "Password",
        render_kw={"placeholder": "Password"},
    )
    email = EmailField(
        "Email", validators=[DataRequired()], render_kw={"placeholder": "Email"}
    )
    submit = SubmitField("Update")

    def validate_password(self, field):
        if type(field.data) is str:
            if field.data != "" and len(field.data) < 6:
                raise ValidationError("The password must contain at least 6 characters.")
        else:
            raise ValidationError("Invalid.")
