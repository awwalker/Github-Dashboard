import os

from flask import Flask, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from github import Github

_GIT = None
csrf = CSRFProtect()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            GIT_TOKEN=os.getenv('GITHUB_TOKEN'),
            )
    # Allow better setting of SECRET_KEY in prod.
    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile('config.py', silent=True)

    # Add CSRF protections to forms. Uses SECRET_KEY as WTF_CSRF_SECRET_KEY.
    csrf.init_app(app)

    from . import search
    app.register_blueprint(search.bp)
    global _GIT
    _GIT=Github(app.config.get('GIT_TOKEN'))
    @app.route('/')
    def index():
        return redirect(url_for('search.search'))
    return app
