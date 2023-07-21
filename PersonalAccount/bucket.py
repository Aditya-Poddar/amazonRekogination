import boto3
import time

# Replace 'your-video-bucket' and 'your-video-key' with your actual S3 bucket name and video object key.
video_bucket = 'rekognitionaditya'
video_key = 'Fundamental01.mp4'

# Initialize the Rekognition client
rekognition = boto3.client('rekognition')

# Start the person tracking job
response = rekognition.start_person_tracking(
    Video={
        'S3Object': {
            'Bucket': video_bucket,
            'Name': video_key
        }
    },
    # NotificationChannel={
    #     'RoleArn': 'your-sns-topic-arn',  # Optional, if you want to receive job status updates
    #     'SNSTopicArn': 'your-sns-role-arn'
    # }
)

# Get the job ID
job_id = response['JobId']
print("JOB ID : ",job_id)
# Wait for the job to complete
while True:
    response = rekognition.get_person_tracking(JobId=job_id)
    status = response['JobStatus']
    
    if status == 'SUCCEEDED':
        print("Person tracking job completed successfully.")
        break
    elif status == 'FAILED':
        print("Person tracking job failed.")
        break
    
    print("Job status: ", status)
    time.sleep(20)  # Wait for 5 seconds before checking the status again

# print the job id
print("JOB ID : ",job_id)

# Get the results
results = response['Persons']

# Now you can analyze the 'results' variable and extract the information you need.
