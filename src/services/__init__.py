def init():
    from dependify import register
    from settings.logs import logger
    from .application.file_service import FileService
    from .infrastructure.s3_file_service import S3FileService

    register(FileService, S3FileService, cached=True)

    logger().debug("Services module initialized")
