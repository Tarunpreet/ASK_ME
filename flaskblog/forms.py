from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    
    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError('That username is taken. Please choose a different one.')

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Send Email')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    # def validate_username(self, username):
    #     if username.data != current_user.username:
    #         user = User.query.filter_by(username=username.data).first()
    #         if user:
    #             raise ValidationError('That username is taken. Please choose a different one.')

    # def validate_email(self, email):
    #     if email.data != current_user.email:
    #         user = User.query.filter_by(email=email.data).first()
    #         if user:
    #             raise ValidationError('That email is taken. Please choose a different one.')

class PostForm(FlaskForm):

    title= StringField('Title', validators=[DataRequired()])
    content=TextAreaField('Content',validators=[DataRequired()])
    tag1=StringField('Tag 1')
    tag2=StringField('Tag 2')
    tag3=StringField('Tag 3')
    submit=SubmitField('Add Question')
    submit2=SubmitField('Predict')

class OnlyPostForm(FlaskForm):

    title= StringField('Title', validators=[DataRequired()])
    content=TextAreaField('Content',validators=[DataRequired()])
    tag1=StringField('Tag 1', validators=[DataRequired()])
    tag2=StringField('Tag 2')
    tag3=StringField('Tag 3')
    submit=SubmitField('Add Question')

class AddAnswer(FlaskForm):

    content=TextAreaField('Content',validators=[DataRequired()])
    submit=SubmitField('ADD ANSWER')