from baseopensdk import BaseClient
from baseopensdk.api.base.v1 import *
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

APP_TOKEN = os.environ['APP_TOKEN']
PERSONAL_BASE_TOKEN = os.environ['PERSONAL_BASE_TOKEN']
TABLE_ID = os.environ['TABLE_ID']

def search_and_replace(source: str, target: str):
  # 1. build client
  client: BaseClient = BaseClient.builder() \
    .app_token(APP_TOKEN) \
    .personal_base_token(PERSONAL_BASE_TOKEN) \
    .build()
  
  # 2. obtain fields info
  list_field_request = ListAppTableFieldRequest.builder() \
    .page_size(100) \
    .table_id(TABLE_ID) \
    .build()

  list_field_response = client.base.v1.app_table_field.list(list_field_request)
  fields = getattr(list_field_response.data, 'items', [])
  text_field_names = [field.field_name for field in fields if field.ui_type == 'Text']

  # 3. iterate over all records
  list_record_request = ListAppTableRecordRequest.builder() \
    .page_size(100) \
    .table_id(TABLE_ID) \
    .build()

  list_record_response = client.base.v1.app_table_record.list(list_record_request)
  records = getattr(list_record_response.data, 'items', [])

  records_need_update = []

  for record in records:
    record_id, fields = record.record_id, record.fields
    new_fields = {}

    for key, value in fields.items():
      # replace value
      if key in text_field_names:
        new_value = value.replace(source, target)
        # add into newFields if needed
        new_fields[key] = new_value if new_value != value else value
    
    if len(new_fields.keys()) > 0:
      records_need_update.append({
        "record_id": record_id,
        "fields": new_fields
      })

  print(records_need_update)

  # 4. batch update records
  batch_update_records_request = BatchUpdateAppTableRecordRequest().builder() \
    .table_id(TABLE_ID) \
    .request_body(
      BatchUpdateAppTableRecordRequestBody.builder() \
        .records(records_need_update) \
        .build()
    ) \
    .build()
  batch_update_records_response = client.base.v1.app_table_record.batch_update(batch_update_records_request)
  print('success!')
  

if __name__ == "__main__":
  # replace all 'abc' to '233333'
  search_and_replace('abc', '233333')