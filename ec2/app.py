# Import boto3, the AWS SDK for Python.
# This allows Python to communicate with AWS services.
import boto3

# Import json to read and format JSON data.
import json


# Define the name of the S3 bucket.
# Replace this placeholder with your actual S3 bucket name.
BUCKET_NAME = "YOUR_S3_BUCKET_NAME"


# Create an S3 client.
# This establishes a connection to Amazon S3 through boto3.
s3 = boto3.client("s3")


# Define a function that retrieves and displays processed files.
def list_processed_files():

    # Ask Amazon S3 to list objects inside our specified bucket.
    # Prefix="processed/" means only retrieve files
    # stored inside the processed/ folder.
    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix="processed/"
    )

    # Extract the list of files from the S3 response.
    # "Contents" contains information about the objects.
    # If no files exist, return an empty list instead.
    files = response.get("Contents", [])

    # Loop through each file found in the S3 folder.
    for file in files:

        # Extract the filename (object key) from the current file.
        key = file["Key"]

        # Retrieve the actual file from the S3 bucket.
        result = s3.get_object(
            Bucket=BUCKET_NAME,
            Key=key
        )

        # Read the file contents and convert the JSON data
        # into a Python dictionary or list.
        report = json.loads(
            result["Body"].read()
        )

        # Convert the Python data back into readable JSON.
        # indent=4 formats the output with four spaces
        # to make it easier to read.
        print(json.dumps(report, indent=4))


# Check whether this Python file is being executed directly.
# If it is, run the list_processed_files() function.
# This prevents the function from running automatically
# when this file is imported into another Python file.
if __name__ == "__main__":

    # Execute the function to retrieve and display processed files.
    list_processed_files()
