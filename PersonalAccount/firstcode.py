import boto3
import time

# Replace 'your-video-bucket' and 'your-video-key' with your actual S3 bucket name and video object key.
video_bucket = 'rekognitionaditya'
video_key = 'Fundamental01.mp4'

# Initialize the Rekognition client
rekognition = boto3.client('rekognition')

# Start the face detection job
response = rekognition.start_face_detection(
    Video={
        'S3Object': {
            'Bucket': video_bucket,
            'Name': video_key
        }
    },
    FaceAttributes='ALL',  # Optional, specify if you want additional face attributes
    # NotificationChannel={
    #     'RoleArn': 'your-sns-topic-arn',  # Optional, if you want to receive job status updates
    #     'SNSTopicArn': 'your-sns-role-arn'
    # }
)

# Get the job ID
job_id = response['JobId']
print(job_id)
# Wait for the job to complete (You can add more sophisticated handling here)
rekognition.get_waiter('SUCCEEDED').wait(JobId=job_id)

print(job_id)
# Get the results
results = rekognition.get_face_detection(JobId=job_id)
print(results)

# Now you can analyze the 'results' variable and extract the information you need.
