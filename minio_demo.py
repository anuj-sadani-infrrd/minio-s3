import time
from urllib.parse import urljoin
import sys
import boto3
from botocore.exceptions import ClientError
import os
import logging

logger = logging.getLogger(__name__)


class MinIOClient:
    def __init__(self, endpoint_url, access_key, secret_key, use_ssl=True):
        self.endpoint_url = endpoint_url
        self.access_key = access_key
        self.secret_key = secret_key
        self.use_ssl = use_ssl
        self.client = boto3.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            use_ssl=self.use_ssl,
        )

    def create_bucket(self, bucket_name):
        try:
            self.client.create_bucket(Bucket=bucket_name)
            logger.info(f"Bucket {bucket_name} created successfully.")
        except ClientError as e:
            logger.error(f"Error: {e}")

    def list_buckets(self):
        try:
            response = self.client.list_buckets()
            buckets = [bucket["Name"] for bucket in response["Buckets"]]
            logger.info(f"Buckets found: {buckets}")
            return buckets
        except ClientError as e:
            logger.error(f"ClientError while listing buckets: {e}")
        except Exception as e:
            logger.error(f"Exception while listing buckets: {e}")

    def list_objects(self, bucket_name):
        try:
            response = self.client.list_objects_v2(Bucket=bucket_name)
            object_keys = [obj["Key"] for obj in response.get("Contents", [])]
            logger.info(f"Objects in bucket '{bucket_name}': {object_keys}")
            return object_keys
        except ClientError as e:
            logger.error(f"ClientError while listing objects in bucket '{bucket_name}': {e}")
        except Exception as e:
            logger.error(f"Exception while listing objects in bucket '{bucket_name}': {e}")

    def download_file(self, bucket_name, object_name, file_path):
        try:
            self.client.download_file(bucket_name, object_name, file_path)
            logger.info(f"Downloaded '{object_name}' from bucket '{bucket_name}' to '{file_path}'")
        except ClientError as e:
            logger.error(f"ClientError while downloading file '{object_name}' from bucket '{bucket_name}': {e}")
        except Exception as e:
            logger.error(f"Exception while downloading file '{object_name}' from bucket '{bucket_name}': {e}")

    def upload_file(self, file_path, bucket_name, object_name, max_retries=3, retry_delay=2):
        logger.info(f"Upload the file: {file_path}")
        for attempt in range(1, max_retries + 1):
            try:
                self.client.upload_file(file_path, bucket_name, object_name)
                logger.info(
                    f"Uploaded file from path: {file_path}\n"
                    f"Endpoint URL --> {self.client.meta.endpoint_url}\n"
                    f"Bucket --> {bucket_name}\n"
                    f"Object name --> {object_name}"
                )
                file_url = urljoin(self.client.meta.endpoint_url, "/".join([bucket_name, object_name]))
                logger.info(f"URL generated --> {file_url}")
                return file_url
            except ClientError as e:
                logger.error(f"ClientError: {e}")
                if attempt == max_retries:
                    return ""
            except Exception as e:
                logger.error(f"Exception: {e}")
                return ""
            time.sleep(retry_delay)

    def upload_dir(self, dir_path, bucket_name, max_retries=3, retry_delay=2):
        try:
            for root, _, files in os.walk(dir_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    object_name = os.path.relpath(file_path, start=dir_path)
                    self.upload_file(file_path, bucket_name, object_name, max_retries, retry_delay)
                    logger.info(f"Uploaded '{file_name}' to MinIO.")
        except Exception as e:
            logger.error(f"Exception while uploading directory '{dir_path}': {e}")

    def delete_file(self, bucket_name, object_name):
        try:
            self.client.delete_object(Bucket=bucket_name, Key=object_name)
            logger.info(f"Deleted file '{object_name}' from bucket '{bucket_name}'")
        except ClientError as e:
            logger.error(f"ClientError while deleting file '{object_name}' from bucket '{bucket_name}': {e}")
        except Exception as e:
            logger.error(f"Exception while deleting file '{object_name}' from bucket '{bucket_name}': {e}")

    def delete_bucket(self, bucket_name):
        try:
            # List all objects in the bucket
            objects = self.client.list_objects(Bucket=bucket_name)

            # Delete all objects in the bucket
            for obj in objects.get("Contents", []):
                self.client.delete_object(Bucket=bucket_name, Key=obj["Key"])

            # Delete the bucket
            self.client.delete_bucket(Bucket=bucket_name)
            logger.info(f"Deleted bucket '{bucket_name}'")
        except ClientError as e:
            logger.error(f"ClientError while deleting bucket '{bucket_name}': {e}")
        except Exception as e:
            logger.error(f"Exception while deleting bucket '{bucket_name}': {e}")


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    MINIO_ENDPOINT = "http://127.0.0.1:9000"
    ACCESS_KEY = "aUzRS6MbEKshAZP0pT71"
    SECRET_KEY = "ewJniPyfTDlYmyhVvOfDPIlvZTKizTVdV6E5Ihjp"

    minio_client = MinIOClient(MINIO_ENDPOINT, ACCESS_KEY, SECRET_KEY)

    # Create 3 buckets
    bucket_names = [f"my-bucket-{i}" for i in range(1, 4)]
    for bucket_name in bucket_names:
        minio_client.create_bucket(bucket_name)

    # List buckets
    buckets = minio_client.list_buckets()
    logger.info(f"Buckets: {buckets}")

    # Upload a file sample.txt to bucket 1
    file_path = "sample.txt"
    bucket_name = bucket_names[0]
    object_name = os.path.basename(file_path)
    minio_client.upload_file(file_path, bucket_name, object_name)

    # Upload a dir docs with 2 json files data-1.json, data-2.json
    dir_path = "docs"
    bucket_name = bucket_names[1]
    minio_client.upload_dir(dir_path, bucket_name)

    # Get the sample.txt
    file_path = "downloaded_sample.txt"
    bucket_name = bucket_names[0]
    object_name = "sample.txt"
    minio_client.download_file(bucket_name, object_name, file_path)

    # List bucket-2 content
    bucket_name = bucket_names[1]
    objects = minio_client.list_objects(bucket_name)
    logger.info(f"Objects in bucket '{bucket_name}': {objects}")

    # delete a file
    bucket_name = bucket_names[0]
    object_name = "sample.txt"
    objects = minio_client.delete_file(bucket_name, object_name)
    logger.info(f"Objects in bucket '{bucket_name}': {objects}")

    # Delete a bucket
    bucket_name = bucket_names[1]
    minio_client.delete_bucket(bucket_name)

    # List buckets
    buckets = minio_client.list_buckets()
