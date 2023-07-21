import boto3
import time

# Replace 'your-video-bucket' and 'your-video-key' with your actual S3 bucket name and video object key.
video_bucket = 'rekognitionaditya'
video_key = 'Bahubali2.mp4'

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
    time.sleep(5)  # Wait for 5 seconds before checking the status again

# print the job id
print("JOB ID : ",job_id)

# Get the results
persons = response['Persons']

# Extract faces' bounding boxes from the person tracking results
faces = []
for person in persons:
    if 'Face' in person:
        faces.extend(person['Face']['BoundingBox'])

# Use DetectFaces to get emotion analysis for each face
emotions = []
for face in faces:
    response = rekognition.detect_faces(
        Image={
            'S3Object': {
                'Bucket': video_bucket,
                'Name': video_key
            }
        },
        Attributes=['ALL']
    )

    if 'FaceDetails' in response:
        face_details = response['FaceDetails']
        for detail in face_details:
            emotions.extend(detail['Emotions'])

# Now you can analyze the 'emotions' list to determine the emotions detected in the video.
