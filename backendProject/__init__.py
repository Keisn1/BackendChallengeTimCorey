import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the App
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "backendProject.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test_config if passed
        app.config.from_mapping(test_config)

    # ensure that the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .db import init_app

    init_app(app)

    from .views import auth

    app.register_blueprint(auth.bp)

    @app.route("/hello")
    @app.route("/")
    def hello():
        return "Hello World\n"

    return app
