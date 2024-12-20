from baseopensdk import BaseClient
from baseopensdk.api.drive.v1 import *
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

APP_TOKEN = os.environ['APP_TOKEN']
PERSONAL_BASE_TOKEN = os.environ['PERSONAL_BASE_TOKEN']
TABLE_ID = os.environ['TABLE_ID']

client = BaseClient.builder() \
    .app_token(APP_TOKEN) \
    .personal_base_token(PERSONAL_BASE_TOKEN) \
    .build()
    
    
# build request
file_name = 'test.txt'
path = os.path.abspath(file_name)
file = open(path, "rb")
request = UploadAllMediaRequest.builder() \
    .request_body(UploadAllMediaRequestBody.builder()
        .file_name(file_name)
        .parent_type("bitable_file")
        .parent_node(APP_TOKEN)
        .size(os.path.getsize(path))
        .file(file)
        .build()) \
    .build()

# send request
response: UploadAllMediaResponse = client.drive.v1.media.upload_all(request)

file_token = response.data.file_token
print(file_token)