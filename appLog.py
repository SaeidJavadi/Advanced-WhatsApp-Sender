import logging
import os
import logging.config
from logging.handlers import SocketHandler
import pythonjsonlogger.jsonlogger
from src import logcolor

if not os.path.exists(fr'.\src\logs'):
    os.mkdir(fr'.\src\logs')
logging.config.fileConfig(fr"src\logging.ini", disable_existing_loggers=True)
log = logging.getLogger(__name__)
try:
    socket_handler = SocketHandler("127.0.0.1", 19996)
except:
    pass
log.addHandler(socket_handler)
