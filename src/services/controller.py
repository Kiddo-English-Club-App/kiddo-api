from flask import Blueprint, request
from dependify import inject

from .application.file_service import FileService


controller = Blueprint('services', __name__, url_prefix='/services')


@controller.get('/files/<string:file_name>')
@inject
def get_file(file_name: str, file_service: FileService):
    file = file_service.get_file(file_name)
    return file.content, 200, {'Content-Type': file.mime_type}

