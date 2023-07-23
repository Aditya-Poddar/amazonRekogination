import boto3
import time

# Create an Amazon Rekognition client
rekognition_client = boto3.client('rekognition', region_name='ap-south-1')

# Replace 'your_bucket_name' and 'your_video_key' with the S3 bucket and object key of your video file.
bucket_name = 'rekognitionaditya'
video_key = 'Fundamental01.mp4'

# Start face detection on the video
response = rekognition_client.start_face_search(
    Video={
        'S3Object': {
            'Bucket': bucket_name,
            'Name': video_key
        }
    },
    FaceAttributes='ALL'
   
)

# Get the job ID for face detection
job_id = response['JobId']
print(f"Face detection job started with ID: {job_id}")

# Wait for the face detection job to complete
while True:
    job_details = rekognition_client.get_face_search(JobId=job_id, MaxResults=1)
    job_status = job_details['JobStatus']
    
    if job_status == 'SUCCEEDED':
        print("Face detection job completed!")
        break
    elif job_status == 'FAILED' or job_status == 'PARTIAL_SUCCESS':
        print(f"Face detection job failed or partially succeeded. Status: {job_status}")
        break
    else:
        print("Face detection job in progress. Please wait...")
        time.sleep(20)  # Wait for 20 seconds before checking the job status again.

# Get the face detection results
results = rekognition_client.get_face_search(JobId=job_id, MaxResults=1000)
print(results)

