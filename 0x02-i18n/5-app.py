#!/usr/bin/env python3
"""Mock logging in
"""
from flask import Flask, g, render_template, request
from flask_babel import Babel


class Config:
    """Representation of babel locale config
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.localeselector
def get_locale():
    """Get locale from client request
    """
    locale = request.args.get('locale', '')

    if locale and locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


# babel.init_app(app, locale_selector=get_locale)


def get_user():
    """Get user by ID passed through URL
    """
    login_id = request.args.get("login_as")

    if login_id:
        return users.get(int(login_id))
    return None


@app.before_request
def before_request():
    """Run before request
    """
    g.user = get_user()


@app.route('/')
def login():
    """Say hello world
    """
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
