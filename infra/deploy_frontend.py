import boto3

ec2 = boto3.resource('ec2', region_name='ap-south-1')

# Replace with your values
AMI_ID = "ami-0f918f7e67a3323f0"   # Amazon Linux 2
INSTANCE_TYPE = "t2.micro"
KEY_NAME = "MERN_microservices_key"   # already created
SECURITY_GROUP_ID = "sg-062040be30e319be3"   # allow SSH + HTTP
SUBNET_ID = "subnet-0aaabfe53665733e6"

# User data script (runs when instance starts)
USER_DATA_SCRIPT = """#!/bin/bash
yum update -y
amazon-linux-extras install docker -y
service docker start
usermod -aG docker ec2-user
# Login to ECR
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 388779989161.dkr.ecr.ap-south-1.amazonaws.com
# Pull frontend image
docker pull 388779989161.dkr.ecr.ap-south-1.amazonaws.com/frontend:latest
# Run frontend container on port 80
docker run -d -p 80:3000 388779989161.dkr.ecr.ap-south-1.amazonaws.com/frontend:latest
"""

# Launch EC2 instance
instances = ec2.create_instances(
    ImageId=AMI_ID,
    InstanceType=INSTANCE_TYPE,
    KeyName=KEY_NAME,
    SecurityGroupIds=[SECURITY_GROUP_ID],
    SubnetId=SUBNET_ID,
    MinCount=1,
    MaxCount=1,
    UserData=USER_DATA_SCRIPT,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'frontend-service'}]
        }
    ]
)

instance = instances[0]
print(f"🚀 Launching EC2 instance {instance.id} for frontend...")
instance.wait_until_running()
instance.reload()
print(f"✅ Frontend deployed at http://{instance.public_dns_name}")
