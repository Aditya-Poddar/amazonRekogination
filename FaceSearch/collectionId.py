import boto3

# Create an Amazon Rekognition client
rekognition_client = boto3.client('rekognition', region_name='ap-south-1')

# Replace 'your_collection_id' with the desired ID for your Amazon Rekognition collection.
collection_id = 'aditya_collection_id'

# Create the collection
try:
    response = rekognition_client.create_collection(CollectionId=collection_id)
    print(f"Collection '{collection_id}' created successfully!")
except rekognition_client.exceptions.ResourceAlreadyExistsException:
    print(f"Collection '{collection_id}' already exists.")
except Exception as e:
    print(f"Error creating collection: {e}")
