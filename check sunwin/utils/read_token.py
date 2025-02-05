import configparser
def read_token_from_ini(filepath):
    config = configparser.ConfigParser()
    config.read(filepath)
    token = config.get('TOKEN', 'token')
    return token