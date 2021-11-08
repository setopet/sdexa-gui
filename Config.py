CONFIG = {}

dev_config = {
    'DEV': True,
    'UPLOAD_DIR': 'uploads/',
    'BASE_URL': 'http://localhost:5000/'
}


#  TODO
def load_config():
    for key, value in dev_config.items():
        CONFIG[key] = value
    return
