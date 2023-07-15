
from google.cloud import storage
from datetime import datetime
import pandas as pd
import json
import sys

class c_data_gbucket:

    def __init__(self):
        self.folder_name='/home/dfbrownnz/example-youtube/'
        self.file_name='employee_records.json'
        self.dtnow = datetime.today().strftime('%Y%m%d %H%M%S')

    def test(self  ):
        print(f" this is c_data_json {self.folder_name}{self.file_name}" )
        self.write_read_my()

    def read_df(self):
        bucket_name='example-bucket-1-dfb'
        blob_name=f'Financial_Report_tsla.xlsx'
        blob_name='Financial_Report_tsla.xlsxConsolidated_Statements_Oper.csv'

        df = self.pandas_read(bucket_name, blob_name)

        # storage_client = storage.Client()
        # bucket = storage_client.bucket(bucket_name)
        # blob = bucket.blob(blob_name)
        # data_bytes = blob.download_as_bytes()

        return str(df.columns)


    def meta_list_buckets(self):
        """Lists all buckets."""

        storage_client = storage.Client()
        buckets = storage_client.list_buckets()
        bucket_list='<br>bucket.name <br>'

        for bucket in buckets:
            print(f'meta_list_buckets in this project {bucket.name} ')
            #bucket_list.append(bucket.name)
            bucket_list+='' + bucket.name + '<br>'
        return bucket_list


    def meta_list_blobs(self, bucket_name):
        """Lists all the files aka blobs in a bucket."""
        # bucket_name = "your-bucket-name"

        storage_client = storage.Client()

        # Note: Client.list_blobs requires at least package version 1.17.0.
        blobs = storage_client.list_blobs(bucket_name)
        #file_list='<br>bucket_name | blob.name <br>'
        file_list=[]

        # Note: The call returns a response only when the iterator is consumed.
        for blob in blobs:
            #print(f'meta_list_blobs in bucket {bucket_name} has blob.name {blob.name}')
            #file_list.append(blob.name)
            #file_list+='| ' + f'{blob.name}'
            #file_list+=bucket_name +  '|' + blob.name + '<br>'
            file_list.append( blob.name  )
        df = pd.DataFrame({ 'File Viewer': file_list })
        df['bucket_name'] = bucket_name
        df = df[['bucket_name', 'File Viewer']]
        return df

    """Sample that creates and consumes a GCS blob using pandas with file-like IO
    """
    # [START storage_fileio_pandas_write]

    def pandas_write(self, bucket_name, blob_name):
        """Use pandas to interact with GCS using file-like IO"""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"

        # The ID of your new GCS object
        # blob_name = "storage-object-name"

        # from google.cloud import storage
        # import pandas as pd

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        with blob.open("w") as f:
            df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
            df['ts']=self.dtnow
            f.write(df.to_csv(index=False))

        #print(f"Wrote csv with pandas with name {blob_name} from bucket {bucket.name}.")


    def get_uniform_bucket_level_access(self, bucket_name):
        """Get uniform bucket-level access for a bucket"""
        # bucket_name = "my-bucket"
        return_val=dict()

        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        iam_configuration = bucket.iam_configuration

        if iam_configuration.uniform_bucket_level_access_enabled:
            return_val['Uniform bucket-level access'] =   f" is enabled for {bucket.name}." 
            #return_val['Bucket will be locked on'] =   f"  {format(iam_configuration.uniform_bucket_level_locked_time)} "
        else:
            return_val['Uniform bucket-level access'] =   f" is NOT enabled for {bucket.name}." 
        return return_val

    # [END storage_fileio_pandas_write]


    # [START storage_fileio_pandas_read]


    def pandas_read(self, bucket_name, blob_name):
        """Use pandas to interact with GCS using file-like IO"""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"

        # The ID of your new GCS object
        # blob_name = "storage-object-name"

        # from google.cloud import storage
        # import pandas as pd

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        df =pd.DataFrame()
        with blob.open("r") as f:
            df = pd.read_csv(f)

        print(f"Read csv with pandas with name {blob_name} from bucket {bucket.name}.")
        df.fillna('', inplace=True)
        return df 

    def write_read_my(self):
        bucket_name='example-bucket-1-dfb'
        blob_name=f'somefile_{self.dtnow}_.txt'
        #self.write_read(bucket_name , blob_name)

    def write_read(self, bucket_name, blob_name):
        """Write and read a blob from GCS using file-like IO"""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"

        # The ID of your new GCS object
        # blob_name = "storage-object-name"

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # Mode can be specified as wb/rb for bytes mode.
        # See: https://docs.python.org/3/library/io.html
        with blob.open("w") as f:
            f.write("Hello world")

        with blob.open("r") as f:
            print(f.read())
    
    def write_file_json(self, bucket_name , file_name):
        
        #bucket_name = 'gcs_bucket_user'
        bucket = storage.Client().get_bucket(bucket_name)
        
        employee_records= {
            "employee": [

                {
                    "id": "11",
                    "name": "Amit ->" + self.dtnow ,
                    "department": "Sales"
                },

                {
                    "id": "14",
                    "name": "sunil ->" + self.dtnow ,
                    "department": "HR"
                }
            ]
        }
        # define a dummy dict
        some_json_object = {'foo': list()}

        for i in range(0, 5):
            some_json_object['foo'].append(i)

        #blob = bucket.blob('text.json') # file_name
        blob = bucket.blob(file_name) # file_name
        # take the upload outside of the for-loop otherwise you keep overwriting the whole file
        blob.upload_from_string(data=json.dumps(employee_records),content_type='application/json') 

    def write_file_json_data(self, bucket_name , file_name, data):
        bucket = storage.Client().get_bucket(bucket_name)
        blob = bucket.blob(file_name) # file_name
        # take the upload outside of the for-loop otherwise you keep overwriting the whole file
        blob.upload_from_string(data=json.dumps(data),content_type='application/json') 


    def json_append(self, bucket_name , file_name, data, record):
        """ """
        # data = self.read_file_json(bucket_name , file_name)
        # employee_record_new = {"id": "007", "name": "james", "department": "HR"}
        data['employee'].append(record)
        self.write_file_json_data(bucket_name , file_name, data)


        
    def json_update(self, bucket_name , file_name):
        """ """
        data = self.read_file_json(bucket_name , file_name)
        employee_record_new = {"id": "007", "name": "james", "department": "HR"}
        data['employee'].append(employee_record_new)
        self.write_file_json_data(bucket_name , file_name, data)

        
        #bucket_name = 'gcs_bucket_user'

    def read_file_json(self, bucket_name , file_name):
        """ """
        
        #bucket_name = 'gcs_bucket_user'
        #bucket = storage.Client().get_bucket(bucket_name)
        # # define a dummy dict
        # some_json_object = {'foo': list()}

        # for i in range(0, 5):
        #     some_json_object['foo'].append(i)

        # #blob = bucket.blob('text.json') # file_name
        # blob = bucket.blob(file_name) # file_name
        # # take the upload outside of the for-loop otherwise you keep overwriting the whole file
        # blob.upload_from_string(data=json.dumps(some_json_object),content_type='application/json') 

        #bucket = client.get_bucket(bucket_name)
        bucket = storage.Client().get_bucket(bucket_name)
        file_blob = storage.Blob(file_name, bucket)
        download_data = file_blob.download_as_string().decode()
        #print("download_data : ", download_data)
        """
        jsondata = {}
        jsondata = download_data
        """
        #convert string to  object
        jsondata = json.loads(download_data)
        #print("jsondata => ", jsondata)
        return jsondata

if __name__ == '__main__':
    file_name='employee_records.json'
    ma = c_data_gbucket()
    ma.test()
    # ma.gstoreage()
