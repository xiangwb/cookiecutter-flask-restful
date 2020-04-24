import click
from flask.cli import FlaskGroup

from {{cookiecutter.app_name}}.app import create_app


def create_{{cookiecutter.app_name}}(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_{{cookiecutter.app_name}})
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Create a new admin user
    """
    from {{cookiecutter.app_name}}.models import User

    click.echo("create user")
    user = User(username="{{cookiecutter.admin_user_username}}", email="{{cookiecutter.admin_user_email}}", password="{{cookiecutter.admin_user_password}}", active=True).save()
    click.echo("created user admin: {id}".format(id=user.id))


if __name__ == "__main__":
    cli()
