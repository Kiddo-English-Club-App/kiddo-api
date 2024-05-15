from flask import Blueprint
from dependify import inject

from {{ module }}.application.{{ module }}_service import {{ class }}Service, dto

controller = Blueprint('{{ module }}', __name__, url_prefix='/{{ plural }}')