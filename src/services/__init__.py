def init():
    from dependify import register
    from settings.environment import env, EnvType
    from settings.logs import logger
    from .application.file_service import FileService
    
    if env.ENV == EnvType.TESTING:
        from .infrastructure.mock_file_service import MockFileService
        register(FileService, MockFileService)
    else:
        from .infrastructure.s3_file_service import S3FileService
        register(FileService, S3FileService, cached=True)

    logger().debug("Services module initialized")
