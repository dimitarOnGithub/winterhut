from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, IPAddress


class IpBanForm(FlaskForm):
    ip_address = StringField("IP Address:", validators=[DataRequired(), IPAddress(ipv4=True, ipv6=False,
                                                                                  message="Please enter a valid IP "
                                                                                          "address")])
    submit = SubmitField("Ban(ana)")


class ImporterForm(FlaskForm):
    file_field = FileField("File")
    submit = SubmitField("Upload")
