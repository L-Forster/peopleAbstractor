import gdrive


def upload():
    secret_key, service = gdrive.init()
    gdrive.upload_db(service, secret_key, gdrive.CURRENT_FOLDER_ID, "DB NAME.db")
    print("Data successfully uploaded")


def phone_load():
    secret_key, service = gdrive.init()
    gdrive.fetch_db(service, secret_key)


def phone_all():
    phone_load()


