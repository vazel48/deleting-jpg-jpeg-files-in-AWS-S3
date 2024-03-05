import boto3

s3 = boto3.client('s3')

bucket_name = 'your_bucket_name'


def delete_jpg_and_jpeg_files(bucket):
    paginator = s3.get_paginator('list_objects_v2')
    delete_us = dict(Objects=[])  # List for storing keys for deletion
    deleted_files_count = 0  # Deleted files counter

    for page in paginator.paginate(Bucket=bucket):
        if "Contents" in page:
            for obj in page['Contents']:
                if obj['Key'].endswith('.jpg') or obj['Key'].endswith('.jpeg'):
                    delete_us['Objects'].append({'Key': obj['Key']})

                    # If 100 objects have accumulated, delete them
                    if len(delete_us['Objects']) >= 100:
                        response = s3.delete_objects(Bucket=bucket, Delete=delete_us)
                        deleted = response.get('Deleted', [])
                        deleted_files_count += len(deleted)
                        for del_obj in deleted:
                            print(f"Deleted: {del_obj['Key']}")
                        delete_us = dict(Objects=[])  # Resetting the list after deletion

    # Deleting the remaining objects, if any still exist
    if len(delete_us['Objects']):
        response = s3.delete_objects(Bucket=bucket, Delete=delete_us)
        deleted = response.get('Deleted', [])
        deleted_files_count += len(deleted)
        for del_obj in deleted:
            print(f"Deleted: {del_obj['Key']}")

    print(f"Total files deleted: {deleted_files_count}")


delete_jpg_and_jpeg_files(bucket_name)
