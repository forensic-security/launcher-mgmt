import logging
import sys

from app.config import settings

try:
    loglevel = getattr(logging, settings.loglevel.upper())
except AttributeError:
    loglevel = logging.DEBUG

logging.captureWarnings(True)
log = logging.getLogger('launcher-mgmt')
log.setLevel(loglevel)
log.propagate = False
ch = logging.StreamHandler(stream=sys.stderr)  # XXX: to show all python logs on docker logs
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)-9s %(asctime)s [%(pathname)s:%(lineno)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
ch.setFormatter(formatter)
log.addHandler(ch)
