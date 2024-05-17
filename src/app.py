from flask import Flask


def load_controllers(app: Flask):
    from flask import Blueprint
    api = Blueprint('api', __name__, url_prefix='/api')
    from account.controller import controller as account_controller
    from theme.controller import controller as theme_controller
    from player.controller import controller as player_controller
    from services.controller import controller as services_controller
    from services.token_controller import controller as token_controller

    api.register_blueprint(account_controller)
    api.register_blueprint(theme_controller)
    api.register_blueprint(player_controller)
    api.register_blueprint(token_controller)
    app.register_blueprint(api)
    app.register_blueprint(services_controller)


def create_app() -> Flask:
    app = Flask(__name__)
    import settings

    settings.init(app)
    load_controllers(app)

    @app.route('/health')
    def health():
        return {"status": "OK"}, 200

    return app