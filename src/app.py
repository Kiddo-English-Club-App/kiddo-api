"""
This module is the entry point of the application. It creates the Flask app and loads the controllers.
"""

from flask import Flask


def load_controllers(app: Flask):
    """
    Loads the controllers into the Flask app. This function should be called at the beginning of the application
    to ensure that all controllers are registered.

    :param app: The Flask app instance
    """
    from flask import Blueprint

    # Import controllers for registration
    api = Blueprint("api", __name__, url_prefix="/api")
    from account.controller import controller as account_controller
    from player.controller import controller as player_controller
    from services.controller import controller as services_controller
    from services.token_controller import controller as token_controller
    from theme.controller import controller as theme_controller

    # Register controllers with the API blueprint
    api.register_blueprint(account_controller)
    api.register_blueprint(theme_controller)
    api.register_blueprint(player_controller)
    api.register_blueprint(token_controller)

    # Register the API blueprint with the app
    app.register_blueprint(api)

    # Register the services controller
    app.register_blueprint(services_controller)


def create_app() -> Flask:
    """
    Creates the Flask application instance.

    :return: The Flask application instance
    """
    app = Flask(__name__)
    import settings
    import settings.dependencies as dependencies
    import settings.environment as environment
    import settings.logs as logs

    # Initialize the application settings (environment, dependencies, error handlers, logs)
    settings.init(app)

    load_controllers(app)

    logs.logger().info(f"Env: {environment.env.ENV}")

    @app.route("/health")
    def health():
        return {"status": "OK", "environment": environment.env.ENV}, 200

    # Add test endpoints if the environment is testing
    # This is useful for testing the application in a CI/CD pipeline
    # The test endpoints allow the database to be initialized and populated with mock data
    if environment.env.is_testing():
        logs.logger().info("Testing environment detected. Adding test endpoints.")

        @app.post("/test")
        def init_test():
            dependencies.delete_db()
            dependencies.populate_db()
            return {"status": "OK"}, 200

        @app.delete("/test")
        def delete_test():
            dependencies.delete_db()
            return {"status": "OK"}, 200

    return app
