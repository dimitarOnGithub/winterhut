from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, IPAddress


class IpBanForm(FlaskForm):
    ip_address = StringField("IP Address:", validators=[DataRequired(), IPAddress(ipv4=True, ipv6=False,
                                                                                  message="Please enter a valid IP "
                                                                                          "address")])
    submit = SubmitField("Ban(ana)")
