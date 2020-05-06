from {{cookiecutter.app_name}}.extensions import pwd_context
from {{cookiecutter.app_name}}.models.mongo import CommonDocument{%- if cookiecutter.use_elasticsearch == "yes" %}, SearchableMixin{%- endif %}
import mongoengine as mg


class User(CommonDocument{%- if cookiecutter.use_elasticsearch == "yes" %}, SearchableMixin{%- endif %}):
    """Basic user model
    """

    username = mg.StringField(required=True, max_length=100, unique=True)
    email = mg.StringField(required=False, max_length=80)
    password = mg.StringField(required=True, max_length=255)
    active = mg.BooleanField(default=True)


    {%- if cookiecutter.use_elasticsearch == "yes" %}
    __searchable__ = ['username', 'email']  # 定义需要es搜索的字段，不定义则不需要es搜索功能
    {%- endif %}

    def clean(self, **kwargs):
        self.password = pwd_context.hash(self.password)

    def __repr__(self):
        return "<User %s>" % self.username
