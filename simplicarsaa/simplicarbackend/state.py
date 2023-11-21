from django.db import models
from django.contrib.auth import get_user_model

STATE_CHOICES = [
    ('AL', 'ALABAMA'),
    ('AK', 'ALASKA'),
    ('AZ', 'ARIZONA'),
    ('AR', 'ARKANSAS'),
    ('CA', 'CALIFORNIA'),
    ('CO', 'COLORADO'),
    ('CT', 'CONNECTICUT'),
    ('DE', 'DELAWARE'),
    ('FL', 'FLORIDA'),
    ('GA', 'GEORGIA'),
    ('HI', 'HAWAII'),
    ('ID', 'IDAHO'),
    ('IL', 'ILLINOIS'),
    ('IN', 'INDIANA'),
    ('IA', 'IOWA'),
    ('KS', 'KANSAS'),
    ('KY', 'KENTUCKY'),
    ('LA', 'LOUISIANA'),
    ('ME', 'MAINE'),
    ('MD', 'MARYLAND'),
    ('MA', 'MASSACHUSETTS'),
    ('MI', 'MICHIGAN'),
    ('MN', 'MINNESOTA'),
    ('MS', 'MISSISSIPPI'),
    ('MO', 'MISSOURI'),
    ('MT', 'MONTANA'),
    ('NE', 'NEBRASKA'),
    ('NV', 'NEVADA'),
    ('NH', 'NEW HAMPSHIRE'),
    ('NJ', 'NEW JERSEY'),
    ('NM', 'NEW MEXICO'),
    ('NY', 'NEW YORK'),
    ('NC', 'NORTH CAROLINA'),
    ('ND', 'NORTH DAKOTA'),
    ('OH', 'OHIO'),
    ('OK', 'OKLAHOMA'),
    ('OR', 'OREGON'),
    ('PA', 'PENNSYLVANIA'),
    ('RI', 'RHODE ISLAND'),
    ('SC', 'SOUTH CAROLINA'),
    ('SD', 'SOUTH DAKOTA'),
    ('TN', 'TENNESSEE'),
    ('TX', 'TEXAS'),
    ('UT', 'UTAH'),
    ('VT', 'VERMONT'),
    ('VA', 'VIRGINIA'),
    ('WA', 'WASHINGTON'),
    ('WV', 'WEST VIRGINIA'),
    ('WI', 'WISCONSIN'),
    ('WY', 'WYOMING'),
]

class State(models.Model):
    state_abbr = models.CharField(max_length=2, choices=STATE_CHOICES)
    state_name = models.CharField(max_length=100)

    def __str__(self):
        return self.state_name

    def save(self, *args, **kwargs):
        for abbreviation, name in STATE_CHOICES:
            if abbreviation == self.state_abbr:
                self.state_name = name
                break
        super().save(*args, **kwargs)