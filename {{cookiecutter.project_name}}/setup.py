from setuptools import setup, find_packages

__version__ = "0.1"

setup(
    name="{{cookiecutter.app_name}}",
    version=__version__,
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "flask",
        "flask-restful",
        "flask-jwt-extended",
        "flask-marshmallow",
        "python-dotenv",
        "pymongo",
        "mongoengine",
        "environs",
        "passlib",
        "apispec[yaml]",
        "apispec-webframeworks",
    ],
    entry_points={
        "console_scripts": [
            "{{cookiecutter.app_name}} = {{cookiecutter.app_name}}.manage:cli"
        ]
    },
)
