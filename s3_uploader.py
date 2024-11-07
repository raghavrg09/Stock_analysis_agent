from io import StringIO
import os
import boto3
from botocore.exceptions import NoCredentialsError
import os
load_dotenv("aws_secret_keys.env")

# Replace these with your actual AWS credentials and bucket name
ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
BUCKET_NAME = # bucket name where to upload the data

def upload_data_to_s3(dataframe, bucket, object_name):
    # Converting to CSV Buffer object
    csv_buffer = StringIO()
    dataframe.to_csv(csv_buffer, index=False)
    data = csv_buffer.getvalue()

    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )

    try:
        s3_client.put_object(Bucket=bucket, Key=object_name, Body=data)
        print(f"Upload of data to {bucket}/{object_name} succeeded.")
    except NoCredentialsError:
        print("Credentials not available.")
