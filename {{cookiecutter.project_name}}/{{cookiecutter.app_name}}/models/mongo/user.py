from {{cookiecutter.app_name}}.extensions import pwd_context
from {{cookiecutter.app_name}}.models.mongo import CommonDocument
import mongoengine as mg


class User(CommonDocument):
    """Basic user model
    """

    username = mg.StringField(required=True, max_length=100, unique=True)
    email = mg.StringField(required=False, max_length=80)
    password = mg.StringField(required=True, max_length=255)
    active = mg.BooleanField(default=True)

    def clean(self, **kwargs):
        self.password = pwd_context.hash(self.password)

    def __repr__(self):
        return "<User %s>" % self.username
