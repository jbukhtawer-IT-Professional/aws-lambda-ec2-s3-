# Import boto3, the AWS SDK for Python.
# This allows Lambda to communicate with AWS services such as S3.
import boto3

# Import json to work with JSON data.
import json

# Import urllib.parse to decode URL-encoded S3 object keys.
import urllib.parse

# Import datetime tools to work with dates and times.
import datetime
from datetime import datetime, timezone


# Create an S3 client.
# This allows our Lambda function to communicate with Amazon S3.
s3 = boto3.client("s3")


# Main Lambda function.
# AWS automatically calls this function when the Lambda is triggered.
# event contains information about what triggered the Lambda.
# context contains information about the Lambda execution environment.
def lambda_handler(event, context):

    # Loop through every S3 event record.
    # An event can contain information about multiple uploaded files.
    for record in event["Records"]:

        # Extract the name of the S3 bucket where the file was uploaded.
        bucket = record["s3"]["bucket"]["name"]

        # Extract the uploaded file's name (object key).
        # unquote_plus decodes special URL characters in the filename.
        # For example, "my+file.txt" becomes "my file.txt".
        key = urllib.parse.unquote_plus(
            record["s3"]["object"]["key"]
        )

        # Print the filename to CloudWatch Logs.
        # This helps us monitor which file Lambda is processing.
        print(f"Processing file: {key}")

        # Retrieve the uploaded file from the S3 bucket.
        response = s3.get_object(
            Bucket=bucket,
            Key=key
        )

        # Get the file's contents.
        # Body contains the actual data stored in S3.
        file_content = response["Body"].read()

        # Decode the file contents into readable text.
        file_text = file_content.decode("utf-8")

        # Print the file contents in CloudWatch Logs.
        print(file_text)

    # Return a success response.
    return {
        "statusCode": 200,
        "body": json.dumps("File processed successfully")
    }
