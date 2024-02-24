import gdrive
from assign_tags import assign_sentences
from init_db import Database


def parse_data():
    # Runs any RoBERTa pipelines to categorise the new sentences. Find a way to find the new sentences..
    # Temporarily set tags or something in sentence to -1.
    # Then get all the sentences with tag '-1' and classify them.
    # Remove the tag '-1' from them.

    # get all unparsed sentences
    db = Database()
    sentence_ids = db.get_unparsed_sentences()
    db.close_connections()
    print(sentence_ids)
    assign_sentences(sentence_ids)

def pc_load():
    secret_key, service = gdrive.init()
    gdrive.fetch_db(service, secret_key)
    parse_data()


def pc_all():
    pc_load()
    upload()


def upload():
    secret_key, service = gdrive.init()
    gdrive.upload_db(service, secret_key, gdrive.CURRENT_FOLDER_ID, "DB NAME.db")
    print("Data successfully uploaded")
