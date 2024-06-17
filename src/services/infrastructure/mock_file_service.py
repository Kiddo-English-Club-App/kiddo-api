import os
from services.application.file_service import File
from shared import exceptions
from settings.environment import env

from ..application.file_service import FileService


class MockFileService(FileService):
    """
    MockFileService is an implementation of the FileService interface that provides methods
    for working with files in a mock environment. It is used for testing and development
    purposes where the actual file system is not accessible.
    """

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
