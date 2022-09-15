import yaml 
import os
from pprint import pprint

config = yaml.safe_load(open("config.yml"))

def path_to_env(path):
    return path.upper()\
        .replace('.','_')

def __get_defined_configs(c = config, current=""):
    if isinstance(c,dict):
        if not current == "":
            current += '.'
        
        paths = []
        for k in c:
            paths += __get_defined_configs(c[k], current+k)
        return paths

    else:
        return [current]

def set_config(path, value):
    global config

    keys = path.split(".")
    result = config
    for i,k in enumerate(keys):
        if i == len(keys)-1:
            result[k] = value
            continue

        if not k in result:
            result[k] = {}
        
        result = result[k]


def get_config(prefix):
    global config

    keys = prefix.split(".")
    result = config
    for k in keys:
        result = result.get(k, None)

    return result

def load_env_configs():
    for path in __get_defined_configs():
        env_c = os.getenv(path_to_env(path))
        if env_c is not None:
            set_config(path, env_c)

load_env_configs()

print("Script configurations:")
pprint(config)
