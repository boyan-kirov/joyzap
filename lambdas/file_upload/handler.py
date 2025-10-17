import base64
import boto3
import json
import datetime
import os
import sys

# Add the parent directory to the path to import helpers
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from helpers.jwt import JWT, AuthorizationError
from helpers.response import Response


def get_file_size(b64string):
    """Calculate the size of a base64 encoded file"""
    return int((len(b64string) * 3) / 4 - b64string.count('=', -2))


def lambda_handler(event, context):
    """
    Lambda handler for file upload functionality.
    Supports both form uploads and gift uploads to S3.
    """
    try:
        jwt_helper = JWT(os.environ["jwt_secret"])
        jwt_helper.auth(event)

        aws_form_upload_folder = os.environ["aws_form_upload_folder"]
        aws_gift_upload_folder = os.environ["aws_gift_upload_folder"]
        aws_bucket = os.environ["aws_bucket"]
        aws_access_key_id = os.environ["aws_access_key_id"]
        aws_secret_access_key = os.environ["aws_secret_access_key"]

        body_data = {}
        if type(event["body"]) is dict:
            body_data = event["body"]
        elif type(event["body"]) is str:
            body_data = json.loads(event["body"])
        else:
            body_data = json.loads(event["body"])

        if body_data.get("is_gift") is not None and body_data.get("is_gift") == True:
            file = body_data["file"]
            file_format, base64_image_data = file.split(';base64,')
            ext = file_format.split('/')[-1]
            data = base64.b64decode(base64_image_data)
            file_name = body_data["file_name"]
            new_file_name = file_name.replace(" ", "_") + "-" + str(datetime.datetime.today().timestamp()).replace(".", "") + "." + ext

            key = "{}/{}".format(aws_gift_upload_folder, new_file_name)

            s3 = boto3.resource('s3',
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key)

            s3.meta.client.head_bucket(Bucket=aws_bucket)
            response_ = s3.Object(aws_bucket, key).put(Body=data)
            file_size = get_file_size(base64_image_data)

            file_path = "https://{}.s3.eu-central-1.amazonaws.com/{}".format(aws_bucket, key)
            body_data["file_link"] = file_path
            body_data["file_name"] = new_file_name
            body_data["file_extension"] = ext
            body_data["file_size"] = file_size
            body_data["s3_data"] = response_
            del body_data["file"]
            return Response.ok(body_data)
        else:
            file = body_data["file"]
            file_format, base64_image_data = file.split(';base64,')
            ext = file_format.split('/')[-1]
            data = base64.b64decode(base64_image_data)
            new_file_name = str(datetime.datetime.today().timestamp()).replace(".", "") + "." + ext

            key = "{}/{}".format(aws_form_upload_folder, new_file_name)

            s3 = boto3.resource('s3',
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key)

            s3.meta.client.head_bucket(Bucket=aws_bucket)
            response_ = s3.Object(aws_bucket, key).put(Body=data, ACL='public-read')
            file_size = get_file_size(base64_image_data)

            file_path = "https://{}.s3.eu-central-1.amazonaws.com/{}".format(aws_bucket, key)
            body_data["file_link"] = file_path
            body_data["file_name"] = new_file_name
            body_data["file_extension"] = ext
            body_data["file_size"] = file_size
            body_data["s3_data"] = response_
            del body_data["file"]
            return Response.ok(body_data)

    except AuthorizationError as e:
        return Response.error(e.status_code, "", "Unauthorized")
    except Exception as e:
        return Response.error(500, str(e), "Internal Server Error")
