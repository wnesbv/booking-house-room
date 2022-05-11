

import os

DEBUG = False
ALLOWED_HOSTS =  ["django-booking-rooms.herokuapp.com"]
DATABASES = {
    "default": {
        "ENGINE": os.getenv("POSTGRESQL_ENGINE"),
        "HOST": os.getenv("POSTGRESQL_HOST"),
        "NAME": os.getenv("POSTGRESQL_NAME"),
        "USER": os.getenv("POSTGRESQL_USER"),
        "PORT": "5432",
        "PASSWORD": os.getenv("POSTGRESQL_PASSWORD"),
        "URI": os.getenv("POSTGRESQL_URI"),
        "Heroku CLI": os.getenv("HEROKU_CLI"),
    },
}
