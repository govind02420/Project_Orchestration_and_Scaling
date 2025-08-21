import boto3

elbv2 = boto3.client('elbv2', region_name='ap-south-1')

# Replace with VPC ID
VPC_ID = "vpc-0fb53498d4739186b"

# Create Target Group for backend
response = elbv2.create_target_group(
    Name="backend-tg",
    Protocol="HTTP",
    Port=5000,  # hello-service (you can create another TG for profile-service if needed)
    VpcId=VPC_ID,
    TargetType="instance",
    HealthCheckProtocol="HTTP",
    HealthCheckPort="5000",
    HealthCheckPath="/",
    Matcher={"HttpCode": "200"}
)

tg_arn = response['TargetGroups'][0]['TargetGroupArn']
print(f"✅ Target Group created with ARN: {tg_arn}")

import boto3

elbv2 = boto3.client('elbv2', region_name='ap-south-1')

# Replace with your VPC ID
VPC_ID = "vpc-0fb53498d4739186b"

# Create Target Group for hello-service
response_hello = elbv2.create_target_group(
    Name="hello-service-tg",   # unique name
    Protocol="HTTP",
    Port=5000, # hello-service port
    VpcId=VPC_ID,     
    TargetType="instance",
    HealthCheckProtocol="HTTP",
    HealthCheckPort="5000",
    HealthCheckPath="/",
    Matcher={"HttpCode": "200"}
)

hello_tg_arn = response_hello['TargetGroups'][0]['TargetGroupArn']
print(f"✅ Target Group created for hello-service: {hello_tg_arn}")

# Create Target Group for profile-service
response_profile = elbv2.create_target_group(
    Name="profile-service-tg",  # unique name
    Protocol="HTTP",
    Port=5001,   # profile-service port
    VpcId=VPC_ID,
    TargetType="instance",
    HealthCheckProtocol="HTTP",
    HealthCheckPort="5001",
    HealthCheckPath="/",
    Matcher={"HttpCode": "200"}
)

profile_tg_arn = response_profile['TargetGroups'][0]['TargetGroupArn']
print(f"✅ Target Group created for profile-service: {profile_tg_arn}")
