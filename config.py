CONFIG = {}

dev_config = {
    'DEV': True,
    'BASE_URL': 'http://localhost:5000/',
    'CHECKPOINT_PATH': './backend/segmentation/checkpoints/0912_194939.ckpt',
    'SECRET_KEY': '010f7321c62f46569f6552d1d7ec1fde'
}


#  TODO
def load_dev_config(app):
    for key, value in dev_config.items():
        CONFIG[key] = value
    app.secret_key = CONFIG['SECRET_KEY']
    return
