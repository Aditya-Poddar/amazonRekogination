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
    FaceAttributes='ALL'  # Request all face attributes, including emotions
)

# Get the job ID
job_id = response['JobId']

# Wait for the job to complete
while True:
    response = rekognition.get_face_detection(JobId=job_id)
    status = response['JobStatus']
    
    if status == 'SUCCEEDED':
        print("Face detection job completed successfully.")
        break
    elif status == 'FAILED':
        print("Face detection job failed.")
        break
    
    print("Job status: ", status)
    time.sleep(20)  # Wait for 20 seconds before checking the status again

# Get the results
faces = response['Faces']

# Analyze the emotions of each person detected
for face in faces:
    print("Face ID:", face['Face']['FaceId'])
    print("Emotions:")
    for emotion in face['Face']['Emotions']:
        print(f"- {emotion['Type']} (Confidence: {emotion['Confidence']:.2f})")
