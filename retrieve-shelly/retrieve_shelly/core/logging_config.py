import logging

def configure_logging() -> None:
    logging.basicConfig(format='%(asctime)s [%(pathname)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().setLevel(logging.INFO)


