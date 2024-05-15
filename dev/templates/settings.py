def init(app):
    from . import environment, dependencies, error_handlers
    """
    Initialize the module
    """
    environment.init(app)
    dependencies.init(app)
    error_handlers.init(app)
    {% for module in modules %}
    from {{ module.module }} import init as {{ module.module }}_init{% endfor %}
    {% for module in modules %}
    {{ module.module }}_init(){% endfor %}
    pass