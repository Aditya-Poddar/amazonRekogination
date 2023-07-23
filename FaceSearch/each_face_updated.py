import boto3
import time

# Create an Amazon Rekognition client
rekognition_client = boto3.client('rekognition', region_name='ap-south-1')

# Replace 'your_bucket_name' and 'your_video_key' with the S3 bucket and object key of your video file.
bucket_name = 'rekognitionaditya'
video_key = 'testvideo.mp4'

# Replace 'your_collection_id' with the ID of your Amazon Rekognition collection.
collection_id = 'aditya_collection_id'

# Start face search on the video
response = rekognition_client.start_face_search(
    CollectionId=collection_id,
    Video={
        'S3Object': {
            'Bucket': bucket_name,
            'Name': video_key
        }
    }
)

# Get the job ID for face search
job_id = response['JobId']
print(f"Face search job started with ID: {job_id}")

# Wait for the face search job to complete
while True:
    job_details = rekognition_client.get_face_search(JobId=job_id, MaxResults=1)
    job_status = job_details['JobStatus']
    
    if job_status == 'SUCCEEDED':
        print("Face search job completed!")
        break
    elif job_status == 'FAILED' or job_status == 'PARTIAL_SUCCESS':
        print(f"Face search job failed or partially succeeded. Status: {job_status}")
        break
    else:
        print("Face search job in progress. Please wait...")
        time.sleep(20)  # Wait for 20 seconds before checking the job status again.

# Get the face search results
results = rekognition_client.get_face_search(JobId=job_id, MaxResults=1000)

# Extract emotions and timestamps for each face
if 'Persons' in results:
    for person in results['Persons']:
        if 'FaceMatches' in person:
            face_matches = person['FaceMatches']
            timestamp_ms = person['Timestamp']
            for face_match in face_matches:
                face_id = face_match['Face']['FaceId']
                face_emotions = face_match['Face']['Emotions']
                
                # Extract and print emotions along with timestamp and face ID
                print(f"Face ID: {face_id}, Timestamp (ms): {timestamp_ms}")
                for emotion in face_emotions:
                    emotion_type = emotion['Type']
                    confidence = emotion['Confidence']
                    print(f"Emotion: {emotion_type}, Confidence: {confidence}")
else:
    print("No faces detected in the video.")
