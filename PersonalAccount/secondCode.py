import boto3

def start_content_moderation(job_name, s3_bucket, s3_object):
    rekognition_client = boto3.client('rekognition')
    response = rekognition_client.start_content_moderation(
        Video={
            'S3Object': {
                'Bucket': s3_bucket,
                'Name': s3_object
            }
        },
        # NotificationChannel={
        #     'SNSTopicArn': 'YOUR_SNS_TOPIC_ARN',
        #     'RoleArn': 'YOUR_SNS_ROLE_ARN'
        # },
        JobTag=job_name
    )
    return response['JobId']

def get_content_moderation_results(job_id):
    rekognition_client = boto3.client('rekognition')
    response = rekognition_client.get_content_moderation(JobId=job_id)
    return response

if __name__ == '__main__':
    # Replace these variables with your own values
    job_name = 'MyContentModerationJob'
    s3_bucket = 'rekognitionaditya'
    s3_object = 'Bahubali2.mp4'

    # Step 1: Start Content Moderation analysis
    job_id = start_content_moderation(job_name, s3_bucket, s3_object)
    print(f"Content Moderation Job ID: {job_id}")

    # Step 2: Check the status and get the results
    content_moderation_results = None
    while content_moderation_results is None:
        response = get_content_moderation_results(job_id)
        content_moderation_results = response.get('ModerationLabels')
        if content_moderation_results is None:
            print("Analysis still in progress...")
    
    # Step 3: Process the results
    if len(content_moderation_results) > 0:
        for label in content_moderation_results:
            print("Moderation label: ", label['ModerationLabel'])
            print("Timestamp: ", label['Timestamp'])
            print("Moderation confidence: ", label['ModerationConfidence'])
            print("Parent category: ", label.get('ParentName', 'N/A'))
            print('--------------------------')
    else:
        print("No content moderation labels found.")
