from flask import Flask


def load_controllers(app: Flask):
    from flask import Blueprint
    api = Blueprint('api', __name__, url_prefix='/api')
    from account.controller import controller as account_controller
    from score.controller import controller as score_controller
    from theme.controller import controller as theme_controller
    from achievement.controller import controller as achievement_controller
    from guest.controller import controller as guest_controller

    api.register_blueprint(account_controller)
    api.register_blueprint(score_controller)
    api.register_blueprint(theme_controller)
    api.register_blueprint(achievement_controller)
    api.register_blueprint(guest_controller)
    app.register_blueprint(api)


def create_app() -> Flask:
    app = Flask(__name__)
    import settings

    settings.init(app)
    load_controllers(app)

    return app