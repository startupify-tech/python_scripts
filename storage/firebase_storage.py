from google.cloud import storage
import os
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv(verbose=True)


class FirebaseStorage:
    def __init__(self):
        credentials_dict = {
            "type": os.getenv('FIREBASE_TYPE'),
            "project_id": os.getenv('FIREBASE_PROJECT_ID'),
            "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
            "private_key": os.getenv('FIREBASE_PRIVATE_KEY'),
            "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
            "client_id": os.getenv('FIREBASE_CLIENT_ID'),
            "auth_uri": os.getenv('FIREBASE_AUTH_URI'),
            "token_uri": os.getenv('FIREBASE_TOKEN_URI'),
            "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
            "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_X509_CERT_URL')
        }
        credentials = service_account.Credentials.from_service_account_info(credentials_dict)
        self.firebase_client = storage.Client(project='duno-10125', credentials=credentials)
        self.bucket = self.firebase_client.get_bucket("duno-10125.appspot.com")

    def upload(self, file_name):
        image_blob = self.bucket.blob("assets/" + file_name)
        image_blob.upload_from_filename(file_name)

    def find_objects(self, file_name):
        blob_list = self.firebase_client.list_blobs(prefix="assets/" + file_name, bucket_or_name=self.bucket.name)
        for blob in blob_list:
            print(blob)
        return blob_list

    def get_signed_url(self, file_name):
        bucket = self.firebase_client.get_bucket(self.bucket.name)
        blob = bucket.get_blob("assets/" + file_name)
        signed_url = blob.generate_signed_url(1609885136)
        print(signed_url)
        return signed_url

    def delete_object(self, file_name):
        bucket = self.firebase_client.get_bucket(self.bucket.name)
        blob = bucket.get_blob("assets/" + file_name)
        blob.delete()


def main():
    store = FirebaseStorage()
    filename = "foxyweeh.png"
    store.upload(filename)
    filename = "foxyweeh"
    found_objects = store.find_objects(filename)
    filename = "foxyweeh.png"
    url = store.get_signed_url(filename)
    store.delete_object(filename)


if __name__ == '__main__':
    main()
