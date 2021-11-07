Config = {}

dev_config = {
    'DEV': True,
    'UPLOAD_DIR': 'uploads/',
    'BASE_URL': 'http://localhost:5000/'
}


#  TODO: Über config.yaml Datei machen der das alles geladen wird + die BaseUrl spezifiziert wird
def load_config():
    for key, value in dev_config.items():
        Config[key] = value
    return
