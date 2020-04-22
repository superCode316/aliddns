from json import loads

config_type = None


def load_config():
    config = open('./config.json')
    c = config.read()
    config.close()
    json_file = loads(c)
    return json_file['ddns']


def set_config(t):
    global config_type
    config_type = t


def read_config(key):
    global config_type
    if config_type:
        configfile = load_config()
        return configfile[key]
    else:
        raise RuntimeError('请设置配置名称')

