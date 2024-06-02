import os
from services.application.file_service import File
from shared import exceptions
from settings.environment import env

from ..application.file_service import FileService


class MockFileService(FileService):

    def get_file(self, file_name: str) -> File:
        name = "mock"
        if file_name.endswith(".jpeg") or file_name.endswith(".jpg"):
            name += ".jpeg"
        elif file_name.endswith(".png"):
            name += ".png"
        elif file_name.endswith(".mp3"):
            name += ".mp3"
        
        if not os.path.exists(f"{env.MOCK_DIR}/{name}"):
            raise exceptions.NotFound(f"File {file_name} not found")

        with open(f"{env.MOCK_DIR}/{name}", "rb") as f:
            mime_type = self.get_mime_type(name)
            return File(file_name, f.read(), mime_type)