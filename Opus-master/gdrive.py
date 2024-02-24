import datetime
import mimetypes
import os

import googleapiclient
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
global db_name
db_name = "INSERT HERE"
CURRENT_FOLDER_ID = " INSERT HERE"
PAST_FOLDER_ID = "INSERT HERE"
SCOPES = ['https://www.googleapis.com/auth/drive']

# Function to pad data to be a multiple of 16 bytes (AES block size)
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def create_key():
    key = get_random_bytes(32)  # Change the number to 16 or 24 for AES-128 or AES-192 respectively
    # Convert the key to a hex representation for storage or usage
    return key


# Function to encrypt data
def encrypt(key, plaintext):
    # Generate a random IV
    iv = get_random_bytes(AES.block_size)
    # Create an AES cipher object with the key and the IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Pad the plaintext to be a multiple of the block size
    padded_plaintext = pad(plaintext, AES.block_size)
    # Encrypt the padded plaintext
    ciphertext = cipher.encrypt(padded_plaintext)
    # Return the IV and the encrypted data together
    return iv + ciphertext


# Function to decrypt data
def decrypt(key, iv_and_ciphertext):
    # Extract the IV from the first 16 bytes
    iv = iv_and_ciphertext[:AES.block_size]
    # Extract the ciphertext from the rest of the data
    ciphertext = iv_and_ciphertext[AES.block_size:]
    # Create an AES cipher object with the key and the IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Decrypt the ciphertext
    padded_plaintext = cipher.decrypt(ciphertext)
    # Unpad the plaintext
    plaintext = unpad(padded_plaintext, AES.block_size)
    return plaintext


def get_file_id(service, folder_id, file_name):
    # Query to search for files with the name in the specific folder
    query = f"parents = '{folder_id}' and name = '{file_name}' and trashed = false"

    # Call the Drive v3 API to search for the file
    response = service.files().list(q=query, spaces='drive',
                                    fields='nextPageToken, files(id, name)').execute()
    files = response.get('files', [])

    if not files:
        print(f"No files with the name '{file_name}' found in the folder.")
        return None# Exit the function as no file was found

    # Assuming only one file should match the criteria, take the first result
    file_id = files[0]['id']
    print(f"Found file: {files[0]['name']} (ID: {file_id})")
    return file_id


def fetch_db(service, secret_key):
    file_id = get_file_id(service, CURRENT_FOLDER_ID, db_name)
    if file_id is None:
        #gets the name of the db with the highest value (i.e. most recent date)
        query = f"parents = '{PAST_FOLDER_ID}' and trashed = false"
        response = service.files().list(q=query, spaces='drive',
                                    fields='nextPageToken, files(id, name)').execute()
        names = []
        for i in range(len(response['files'])):
            names.append(response['files'][i]['name'])
        names.sort()
        file_id = get_file_id(service, PAST_FOLDER_ID, names[0])

    # Download the SQLite file from Google Drive
    request = service.files().get_media(fileId=file_id)
    encrypted_data = request.execute()
    # Decrypt the data
    decrypted_data = decrypt(secret_key, encrypted_data)
    # Write the decrypted data to a file
    with open(os.path.abspath(db_name), 'wb') as file:
        file.write(decrypted_data)
    # move file_id to PAST_FOLDER_ID
    upload_db(service, secret_key, PAST_FOLDER_ID, str(datetime.datetime.now()) + ".db")


# Upload new database to cloud.

def upload_db(service, secret_key, drive_path, upload_name):
    # Encrypt the SQLite file before uploading it back to Google Drive

    file_id = get_file_id(service, drive_path, upload_name)
    with open(os.path.abspath(db_name), 'rb') as file:
        plaintext = file.read()
        encrypted_plaintext = encrypt(secret_key, plaintext)

    # Save encrypted data to a temporary file
    encrypted_file_path = 'encrypted_data.db'  # Choose a suitable file name
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_plaintext)

    # Get MIME type of the encrypted file
    mime_type, _ = mimetypes.guess_type(encrypted_file_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type if it cannot be determined

    # Set metadata for the file to be uploaded
    file_metadata = {'name': upload_name, 'mimeType': mime_type}

    # Upload the modified encrypted SQLite file back to Google Drive
    media = googleapiclient.http.MediaFileUpload(encrypted_file_path, mimetype=mime_type)
    if file_id is not None:
        service.files().update(fileId=file_id, media_body=media, body=file_metadata).execute()
    # if there is no file present in the drive:
    else:
        file_metadata = {'name': upload_name, 'mimeType': mime_type, 'parents': [drive_path]}
        service.files().create(media_body=media, body=file_metadata).execute()


def create_token_json():
    flow = InstalledAppFlow.from_client_secrets_file(
        'SECRET FILE HERE', SCOPES)
    creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())


#main_pc(): fetches data from drive.
# evaluates the sentences
# uploads new drive
def main_pc(service, secret_key, creds):
    # print("Generated AES Key:", secret_key)
    # secret_key = create_key()
    fetch_db(service, secret_key)
    # copy database from current to past.
    upload_db(service, secret_key, CURRENT_FOLDER_ID.path.abspath("DB NAME.db"))


def main_phone(service, secret_key, creds):
    #print("Generated AES Key:", secret_key)
    # secret_key = create_key()
    # fetch_db(service, secret_key)
    # copy database from current to past.
    upload_db(service, secret_key, CURRENT_FOLDER_ID, os.path.abspath("DB NAME.db"))


def phone_fetch_facade(service, secret_key, creds):
    fetch_db(service, secret_key)


def init():
    try:
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    except FileNotFoundError:
        create_token_json()
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Authenticate and create a service for accessing Drive API
    service = build('drive', 'v3', credentials=creds)
    secret_key = create_key()
    print(secret_key)
    return secret_key, service

init()