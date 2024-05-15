from flask import Flask


def load_controllers(app: Flask):
    from flask import Blueprint
    api = Blueprint('api', __name__, url_prefix='/api'){% for module in modules %}
    from {{ module.module }}.controller import controller as {{ module.module }}_controller{% endfor %}
{% for module in modules %}
    api.register_blueprint({{ module.module }}_controller){% endfor %}
    app.register_blueprint(api)


def create_app() -> Flask:
    app = Flask(__name__)
    import settings

    settings.init(app)
    load_controllers(app)

    return app