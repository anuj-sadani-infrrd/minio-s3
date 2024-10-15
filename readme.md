Here’s the updated `README.md` with Step 2 for creating access and secret keys using MinIO's UI and Step 3 for creating buckets via the UI.

---

# MinIO S3 Operations with Docker and Boto3

This repository contains instructions and a Python script (`minio_util.py`) to perform basic S3 operations using MinIO, Docker, and `boto3`. You will be able to set up MinIO locally, create access keys, manage buckets, and upload/download objects using `boto3`.

## Prerequisites

- Docker installed on your machine.
- Python 3.x installed (need version 3.7+).
- `boto3` installed. You can install it using:
  ```bash
  pip install boto3
  ```

## Step 1: Running MinIO in Docker

To set up and run MinIO locally, follow these steps:

1. **Create a directory to persist MinIO data**:

   ```bash
   mkdir -p ${HOME}/minio/data
   ```
2. **Run MinIO using Docker**:

   ```bash
   docker run \
      -p 9000:9000 \
      -p 9001:9001 \
      --user $(id -u):$(id -g) \
      --name minio1 \
      -e "MINIO_ROOT_USER=ROOTUSER" \
      -e "MINIO_ROOT_PASSWORD=CHANGEME123" \
      -v ${HOME}/minio/data:/data \
      quay.io/minio/minio server /data --console-address ":9001"
   ```

   - **MINIO_ROOT_USER**: Set your MinIO root username (default: `ROOTUSER`).
   - **MINIO_ROOT_PASSWORD**: Set your MinIO root password (default: `CHANGEME123`).
   - Access MinIO console at: `http://localhost:9001`

## Step 2: Creating Access and Secret Keys Using MinIO UI

To interact with MinIO using `boto3`, you need an access key and secret key. Here's how to create them using the MinIO web interface:

1. Open your browser and navigate to the MinIO web console at:`http://localhost:9001/access-keys`
2. **Create an Access Key**:

   - Click on "Create Access Key."
   - Enter any desired name or leave it default.
   - Click **Create**.
3. **Copy the Access Key and Secret Key**:

   - A new access key and secret key will be displayed.
   - **Important**: Copy the **secret key** immediately, as it will only be shown once.

   You can now use these keys in your Python script (`minio_util.py`) for connecting to MinIO.

## Step 3: Creating Buckets Using MinIO UI

Once you've set up MinIO and created your keys, follow these steps to create a bucket:

1. Open the MinIO console in your browser at:`http://localhost:9001`
2. Log in using your **ROOTUSER** and **CHANGEME123** credentials (or the credentials you've set up).
3. Navigate to the "Buckets" section:

   - Click **Create Bucket**.
   - Enter a bucket name (e.g., `my-test-bucket`).
   - Click **Create**.

You now have a bucket ready to store objects.

## Step 4: Interacting with MinIO via Python and Boto3

### Python Script: `minio_util.py`

This Python script provides examples for connecting to MinIO and performing S3 operations.

#### Example Operations:

- **List Buckets**
- **Upload an Object**
- **Download an Object**

### Setup Access Keys

In `minio_util.py`, replace the placeholders with your MinIO credentials:

```python
import boto3

# MinIO configuration
minio_client = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='YOUR_ACCESS_KEY',       # Replace with your Access Key
    aws_secret_access_key='YOUR_SECRET_KEY'    # Replace with your Secret Key
)
```

### Running the Script

To perform the S3 operations:

```bash
python minio_demo.py
```

Output

```txt
INFO:__main__:Bucket my-bucket-1 created successfully.
INFO:__main__:Bucket my-bucket-2 created successfully.
INFO:__main__:Bucket my-bucket-3 created successfully.
INFO:__main__:Buckets found: ['my-bucket-1', 'my-bucket-2', 'my-bucket-3']
INFO:__main__:Buckets: ['my-bucket-1', 'my-bucket-2', 'my-bucket-3']
INFO:__main__:Upload the file: sample.txt
INFO:__main__:Uploaded file from path: sample.txt
Endpoint URL --> http://127.0.0.1:9000
Bucket --> my-bucket-1
Object name --> sample.txt
INFO:__main__:URL generated --> http://127.0.0.1:9000/my-bucket-1/sample.txt
INFO:__main__:Upload the file: docs/data-1.json
INFO:__main__:Uploaded file from path: docs/data-1.json
Endpoint URL --> http://127.0.0.1:9000
Bucket --> my-bucket-2
Object name --> data-1.json
INFO:__main__:URL generated --> http://127.0.0.1:9000/my-bucket-2/data-1.json
INFO:__main__:Uploaded 'data-1.json' to MinIO.
INFO:__main__:Upload the file: docs/data-2.json
INFO:__main__:Uploaded file from path: docs/data-2.json
Endpoint URL --> http://127.0.0.1:9000
Bucket --> my-bucket-2
Object name --> data-2.json
INFO:__main__:URL generated --> http://127.0.0.1:9000/my-bucket-2/data-2.json
INFO:__main__:Uploaded 'data-2.json' to MinIO.
INFO:__main__:Downloaded 'sample.txt' from bucket 'my-bucket-1' to 'downloaded_sample.txt'
INFO:__main__:Objects in bucket 'my-bucket-2': ['data-1.json', 'data-2.json']
INFO:__main__:Objects in bucket 'my-bucket-2': ['data-1.json', 'data-2.json']
INFO:__main__:Deleted file 'sample.txt' from bucket 'my-bucket-1'
INFO:__main__:Objects in bucket 'my-bucket-1': None
INFO:__main__:Deleted bucket 'my-bucket-2'
INFO:__main__:Buckets found: ['my-bucket-1', 'my-bucket-3']

```

## Step 5: Accessing MinIO Web Interface

To monitor and manage your buckets and objects visually, you can use MinIO's web interface at:

```
http://localhost:9001
```

Log in with the credentials:

- **Username**: `ROOTUSER`
- **Password**: `CHANGEME123` (or your chosen credentials)

## Conclusion

You now have a MinIO server running locally using Docker, and you can interact with it programmatically using Python and `boto3` for S3 operations like creating buckets, uploading, and downloading objects.
