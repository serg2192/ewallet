import logging.handlers
import logging.config
import os
import pathlib

from marshmallow import Schema, fields
import yaml

from billing.errors import InvalidInputParamsError


BASE_DIR = pathlib.Path(__file__).parent.parent
CONFIG_PATH = os.path.join(BASE_DIR, 'config', 'config.yaml')

logger = logging.getLogger(__name__)


def get_config(path=None):
    path = path or os.getenv('CONFIG_PATH', CONFIG_PATH)
    config_validator = ConfigSchema()
    with open(path) as f:
        config = yaml.safe_load(f)
    errors = config_validator.validate(config)
    if errors:
        # todo: need another code for this
        raise InvalidInputParamsError(details=errors)

    logging.config.dictConfig(config['logging'])
    logger.info(f'Loaded config file: {config}')
    return config


class ConfigSchema(Schema):
    application = fields.Dict(
        required=True,
    )  # Nested may be better
    db = fields.Dict(
        required=True,
    )  # Nested may be better
    logging = fields.Dict(
        required=True,
    )  # Nested may be better
