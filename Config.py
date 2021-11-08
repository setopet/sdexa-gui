CONFIG = {}

dev_config = {
    'DEV': True,
    'UPLOAD_DIR': 'uploads/',
    'BASE_URL': 'http://localhost:5000/',
    'CHECKPOINT_PATH': './backend/segmentation/checkpoints/0912_194939.ckpt'
}


#  TODO
def load_config():
    for key, value in dev_config.items():
        CONFIG[key] = value
    return
