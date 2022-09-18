from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField


class PostForm(FlaskForm):
    title = StringField(label='title')
    body = TextAreaField(label='body')
    submit = SubmitField(label='submit')