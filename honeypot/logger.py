import logging
import os
from logging.handlers import RotatingFileHandler
from main import honeypot_settings

# Logging Format.
logging_format = logging.Formatter('%(asctime)s %(message)s')

# Create the logs directory if it does not exist.
if not os.path.exists(f'{honeypot_settings.log_directory}'):
    os.makedirs(f'{honeypot_settings.log_directory}')

# Funnel (catch all) Logger.
funnel_logger = logging.getLogger('FunnelLogger')
funnel_logger.setLevel(logging.INFO)
funnel_handler = RotatingFileHandler(f'{honeypot_settings.log_directory}/cmd_audits.log', maxBytes=2000, backupCount=5)
funnel_handler.setFormatter(logging_format)
funnel_logger.addHandler(funnel_handler)

# Create the logger
server_logger = logging.getLogger('ServerLogger')
server_logger.setLevel(logging.INFO)

# Create handlers
server_handler = RotatingFileHandler(f'{honeypot_settings.log_directory}/server_log.log', maxBytes=2000, backupCount=5)
console_handler = logging.StreamHandler()

# Set formatter
server_handler.setFormatter(logging_format)
console_handler.setFormatter(logging_format)

# Add handlers to the logger
server_logger.addHandler(server_handler)
server_logger.addHandler(console_handler)

# Credentials Logger. Captures IP Address, Username, Password.
creds_logger = logging.getLogger('CredsLogger')
creds_logger.setLevel(logging.INFO)
creds_handler = RotatingFileHandler(f'{honeypot_settings.log_directory}/creds_audits.log', maxBytes=2000, backupCount=5)
creds_handler.setFormatter(logging_format)
creds_logger.addHandler(creds_handler)