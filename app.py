
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired
from flask_mail import Mail, Message
import secrets


app = Flask(__name__)
Bootstrap(app)

app.secret_key = secrets.token_hex(16)

app.config.update(
    MAIL_SERVER='your_email_server',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='your_email_address',
    MAIL_PASSWORD='your_email_password'
)
mail = Mail(app)

class FilterForm(FlaskForm):
    
    columns = SelectMultipleField("Visible Columns", coerce=str, validators=[DataRequired()])
    custom_filter = SelectField("Custom Filter", choices=[('none', 'None'), ('age_gt_50', 'Age > 50')], default='none')
    column_name = StringField('Column Name', validators=[DataRequired()])
    filter_value = StringField('Filter Value', validators=[DataRequired()])
    submit = SubmitField('Filter')



@app.route('/', methods=['GET', 'POST'])
def index():
    form = FilterForm()
    data = pd.read_csv('Hint Patients - 2023-05-15.csv')

    if form.validate_on_submit():
        column_name = form.column_name.data
        filter_value = form.filter_value.data
        data = data[data[column_name] == filter_value]

    return render_template('index.html', data=data.to_dict(orient='records'), form=form)


@app.route('/send_emails', methods=['POST'])
def send_emails():
    recipients = request.form.getlist('email')
    subject = 'Your Email Subject'
    body = 'Your Email Body'
    msg = Message(subject, recipients=recipients, body=body)
    mail.send(msg)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)