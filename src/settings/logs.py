def init():
    import logging
    from .environment import env, EnvType

    logging.basicConfig(format='%(message)s')
    logging.getLogger().addFilter(logging.Filter('kiddo'))

    logger = logging.getLogger("kiddo")
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.propagate = False
    
    if env.ENV == EnvType.DEVELOPMENT:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

def logger():
    import logging
    return logging.getLogger("kiddo")