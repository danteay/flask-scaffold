"""Configuration methods"""

import os
import pathlib
import json

import yaml
import boto3

NAMESPACE = os.getenv("APP_NAME")


def load():
    """
    Load app configuration depending of STAGE env var.
    If STAGE is equals to `dev`, will attempt to load from local config.yml file.
    If STAGE is equals to `staging` or prod will attempt to load from AWS SecretsManager resource
    named as `<namespace>/<stage>`
    :return: Configuration dict
    """

    stage = os.getenv("STAGE", "dev")

    if stage in ("staging", "prod"):
        return _load_aws(stage)

    return _load_local()


def _load_local():
    """
    Load local config from config.yml file
    :return: Configuration dict
    """

    path = pathlib.Path(__file__).parent.absolute()
    file = f"{path}/config.yml"

    config = open(file)

    data = yaml.load(config, Loader=yaml.FullLoader)

    return data


def _load_aws(stage):
    """
    Load config from AWS SecretsManager resource according STAGE
    :param stage: Stage config to find
    :returns: Configuration dict
    """

    secret_name = f"{NAMESPACE}/{stage}"
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)

    secret = json.loads(get_secret_value_response["SecretString"])

    return secret
