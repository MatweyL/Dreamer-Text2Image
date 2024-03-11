import json
import os
from pathlib import Path
from typing import Type

from pydantic_settings import BaseSettings


def build_rmq_connection_url(
        protocol: str,
        user: str,
        password: str,
        host: str,
        port: str,
        virtual_host: str
):
    host = f"{host}:{port}" if port else host
    connection_url = f"{protocol}://{user}:{password}@{host}/{virtual_host}"
    return connection_url


def build_rmq_default_connection_url():
    return build_rmq_connection_url('ampq', 'guest', 'guest', 'localhost', '5672', '/')


def get_project_root():
    return Path(__file__).parent.parent


def get_env_path():
    return os.path.join(get_project_root(), '.env')


def generate_env_template(settings_base_class: Type[BaseSettings]):
    env_template = ""
    for cls in settings_base_class.__subclasses__():
        env_prefix = cls.model_config['env_prefix']
        for var in cls.model_fields:
            env_var = f'{env_prefix}{var}=\n'
            env_template += env_var
    return env_template


def save_text(dir_path: str | Path, name: str, data: str):
    file_path = os.path.join(dir_path, name)
    with open(file_path, 'w') as text_file:
        text_file.write(data)


def save_json(dir_path: str | Path, name: str, data: dict):
    file_path = os.path.join(dir_path, name)
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2, default=str)


def generate_and_save_env_template(settings_base_class: Type[BaseSettings]):
    save_text(get_project_root(), '.env.template', generate_env_template(settings_base_class))
