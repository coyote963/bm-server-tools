from wtforms import Form, BooleanField, StringField, IntegerField, validators
from wtforms.validators import ValidationError

import re


def only_characters(form, field):
    if not re.match("^[A-Za-z0-9_-]*$", field.data):
        raise ValidationError('Can only contain letters, numbers and dashes')


class RegistrationForm(Form):
    Password = StringField('Password', [only_characters])
    MOTD = StringField('Message of the Day', [only_characters])
    Name = StringField('Server Name', [validators.Optional(), validators.Length(max = 20), only_characters])
    MaxPlayers = IntegerField('Max Players', [validators.Optional(), validators.NumberRange(min = 0, max = 20)]) 
    EnableSpec = BooleanField()
    StrictSpec = BooleanField()
    WarmUp = BooleanField()
    GameMode = IntegerField('Game Mode', [validators.Optional(), validators.NumberRange(min = 0, max = 7)])
    Fiesta = BooleanField()
    Hazards = BooleanField()
    AllWater = BooleanField()