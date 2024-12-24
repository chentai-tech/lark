# Upload the file corresponding to a link field to an attachment field

from baseopensdk import BaseClient
from baseopensdk.api.base.v1 import *
from baseopensdk.api.drive.v1 import *
from dotenv import load_dotenv, find_dotenv
import os
import requests

load_dotenv(find_dotenv())

APP_TOKEN = os.environ['APP_TOKEN']
PERSONAL_BASE_TOKEN = os.environ['PERSONAL_BASE_TOKEN']
TABLE_ID = os.environ['TABLE_ID']

def url_to_attachment():
    # 1. build client
    client: BaseClient = BaseClient.builder() \
        .app_token(APP_TOKEN) \
        .personal_base_token(PERSONAL_BASE_TOKEN) \
        .build()

    # 2. iterate over all records
    list_record_request = ListAppTableRecordRequest.builder() \
        .page_size(100) \
        .table_id(TABLE_ID) \
        .build()

    list_record_response = client.base.v1.app_table_record.list(list_record_request)
    records = getattr(list_record_response.data, 'items', [])

    for record in records:
        record_id, fields = record.record_id, record.fields
        # 3. obtain link field value
        link = (fields.get('Link', {})).get('link')
        if link:
            # 4. download image
            image_resp = requests.get(link, stream=True)
            content = image_resp.content

            # 5. upload file to Drive in exchange for file_token
            request = UploadAllMediaRequest.builder() \
                .request_body(UploadAllMediaRequestBody.builder()
                    .file_name('test.png')
                    .parent_type("bitable_image")
                    .parent_node(APP_TOKEN)
                    .size(len(content))
                    .file(content)
                    .build()) \
                .build()
            response = client.drive.v1.media.upload_all(request)

            file_token = response.data.file_token
            print(file_token)

            # 6. update the attachment field of the corresponding record
            request = UpdateAppTableRecordRequest.builder() \
                .table_id(TABLE_ID) \
                .record_id(record_id) \
                .request_body(AppTableRecord.builder()
                    .fields({
                        "Attachment": [{"file_token": file_token}]
                    })
                    .build()) \
                .build()
            response: UpdateAppTableRecordResponse = client.base.v1.app_table_record.update(request)


if __name__ == "__main__":
    url_to_attachment()