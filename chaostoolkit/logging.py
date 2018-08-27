# -*- coding: utf-8 -*-
import logging

import logzero
from logzero import logger, LogFormatter, setup_default_logger
from pythonjsonlogger import jsonlogger

from chaostoolkit import encoder

__all__ = ["configure_logger"]


def configure_logger(verbose: bool = False, log_format: str = "string",
                     log_file: str = None, logger_name: str = "chaostoolkit"):
    """
    Configure the chaostoolkit logger.

    By default logs as strings to stdout and the given file. When `log_format`
    is `"json"`, records are set to the console as JSON strings but remain
    as strings in the log file. The rationale is that the log file is mostly
    for grepping purpose while records written to the console can be forwarded
    out of band to anywhere else.
    """
    log_level = logging.INFO
    fmt = "%(color)s[%(asctime)s %(levelname)s]%(end_color)s %(message)s"
    if verbose:
        log_level = logging.DEBUG
        fmt = "%(color)s[%(asctime)s %(levelname)s] "\
              "[%(module)s:%(lineno)d]%(end_color)s %(message)s"

    formatter = LogFormatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")
    if log_format == 'json':
        fmt = "(process) (asctime) (levelname) (module) (lineno) (message)"
        formatter = jsonlogger.JsonFormatter(
            fmt, json_default=encoder, timestamp=True)

    # sadly, no other way to specify the name of the default logger publicly
    LOGZERO_DEFAULT_LOGGER = logger_name
    setup_default_logger(level=log_level, formatter=formatter)

    if log_file:
        # always everything as strings in the log file
        logger.setLevel(logging.DEBUG)
        fmt = "%(color)s[%(asctime)s %(levelname)s] "\
              "[%(module)s:%(lineno)d]%(end_color)s %(message)s"
        formatter = LogFormatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")
        logzero.logfile(log_file, formatter=formatter, mode='a',
                        loglevel=logging.DEBUG)
