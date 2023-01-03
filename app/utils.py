import sys
from logging import getLogger, StreamHandler, Formatter, DEBUG

def get_app_logger(module_name):
    formatter = Formatter('%(levelname)s\t %(asctime)s\t %(filename)s\t %(funcName)s\t %(message)s')

    sHandler = StreamHandler(sys.stdout)
    sHandler.setFormatter(formatter)

    logger = getLogger(module_name)
    logger.addHandler(sHandler)
    logger.setLevel(DEBUG)

    return logger

from flask import jsonify
from werkzeug.exceptions import \
    MethodNotAllowed, BadRequest, InternalServerError
logger = get_app_logger(__name__)

def get_exception_status_code(exception):
    json = '{}'
    status_code = 200
    if type(exception) == MethodNotAllowed:
        logger.error(f'Thrown Method Not Allowed Exception : {str(exception)}')
        json = jsonify({'exception': str(exception)})
        status_code = 405
    elif type(exception) == BadRequest:
        logger.error(f'Thrown Bad Request Exception : {str(exception)}')
        json = jsonify({'exception': str(exception)})
        status_code = 400
    elif type(exception) == InternalServerError:
        logger.error(f'Thrown Internal Server Error : {str(exception)}')
        json = jsonify({'exception': str(exception)})
        status_code = 500
    else:
        logger.error(f'Thrown Internal Server Error : {str(exception)}')
        json = jsonify({'exception': str(exception)})
        status_code = 500

    return json, status_code
