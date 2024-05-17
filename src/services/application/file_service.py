import os 

mime_types = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'bmp': 'image/bmp',
    'tiff': 'image/tiff',
    'tif': 'image/tiff',
    'webp': 'image/webp',
    'ico': 'image/x-icon',
    'svg': 'image/svg+xml',
    'heif': 'image/heif',
    'heic': 'image/heic',
    'raw': 'image/x-raw'
}


class File:
    name: str
    content: bytes
    mime_type: str

    def __init__(self, name: str, content: bytes, mime_type: str):
        self.name = name
        self.content = content
        self.mime_type = mime_type


class FileService:

    def get_file(self, file_name: str) -> File:
        pass

    def extract_extension(self, file_name: str) -> str:
        extension = os.path.splitext(file_name)[1]
        if extension:
            return extension[1:].replace(".", "")
        return None
    
    def get_mime_type(self, file_name: str) -> str:
        extension = self.extract_extension(file_name)
        if extension in mime_types:
            return mime_types[extension]
        return "application/octet-stream"

    def cache_file(self, file_name: str, content: bytes):
        if not os.path.exists("cache"):
            os.makedirs("cache")
        
        with open(f"cache/{file_name}", "wb") as file:
            file.write(content)

    
    
    