from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp


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
