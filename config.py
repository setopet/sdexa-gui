
#  TODO: Über config.yaml Datei machen der das alles geladen wird + die BaseUrl spezifiziert wird
def config(app):
    app.config['FILENAME_SURVIEW'] = None
    app.config['FILENAME_CT'] = None
    app.config['UPLOAD_DIR'] = 'uploads'