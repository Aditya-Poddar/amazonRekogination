import time
import boto3

def start_content_moderation(video_s3_bucket, video_s3_key, region_name):
    rekognition_client = boto3.client('rekognition', region_name=region_name)

    response = rekognition_client.start_content_moderation(
        Video={
            'S3Object': {
                'Bucket': video_s3_bucket,
                'Name': video_s3_key
            }
        },
        # NotificationChannel={
        #     'SNSTopicArn': 'YOUR_SNS_TOPIC_ARN',  # Optional: If you want to receive notifications
        #     'RoleArn': 'YOUR_IAM_ROLE_ARN'  # Optional: If you have an existing IAM role for SNS
        # }
    )

    return response['JobId']

def get_content_moderation_results(job_id, region_name):
    rekognition_client = boto3.client('rekognition', region_name=region_name)

    response = rekognition_client.get_content_moderation(JobId=job_id)

    return response

def wait_for_content_moderation_job_completion(job_id, region_name):
    rekognition_client = boto3.client('rekognition', region_name=region_name)

    while True:
        response = rekognition_client.get_content_moderation(JobId=job_id)
        status = response['JobStatus']
        
        if status == 'SUCCEEDED':
            break
        elif status == 'FAILED' or status == 'PARTIAL_SUCCESS':
            raise Exception(f"Content moderation job failed or partially succeeded. Status: {status}")
        
        print(f"Content moderation job status: {status}. Waiting for completion...")
        time.sleep(10)

    return response

def save_response_to_file(response, output_file):
    with open(output_file, 'w') as file:
        file.write(str(response))


if __name__ == '__main__':
    # Replace with your S3 bucket name, video file key, and AWS region
    s3_bucket_name = 'rekognitionaditya'
    video_key = '123.mp4'
    aws_region = 'ap-south-1' 
    output_file = 'response.txt'
    
    # Step 1: Start content moderation analysis
    job_id = start_content_moderation(s3_bucket_name, video_key, aws_region)
    print(f"Content Moderation analysis started. Job ID: {job_id}")

    # Step 2: Wait for the analysis to complete
    response = wait_for_content_moderation_job_completion(job_id, aws_region)
    
    # Step 3: Save the response to a file
    save_response_to_file(response, output_file)
    print(f"Content Moderation Results saved to '{output_file}'.")

    # Step 4: Retrieve and print the results
    print("Content Moderation Results:")
    print(response)
