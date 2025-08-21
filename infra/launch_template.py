import boto3
import base64

ec2 = boto3.client('ec2', region_name='ap-south-1')

with open("userdata.sh", "r") as f:
    userdata_script = f.read()

# Replace with actual values
AMI_ID = "ami-0f918f7e67a3323f0"      # Use latest Ubuntu 22.04 AMI in ap-south-1
INSTANCE_TYPE = "t2.micro"
SECURITY_GROUP_ID = "sg-0e50a35b5d9dc5887"  # from security_group.py 
KEY_NAME = "MERN_microservices_key"  # key pair

response = ec2.create_launch_template(
    LaunchTemplateName="backend-launch-template",
    LaunchTemplateData={
        "ImageId": AMI_ID,
        "InstanceType": INSTANCE_TYPE,
        "KeyName": KEY_NAME,
        "SecurityGroupIds": [SECURITY_GROUP_ID],
        "UserData": base64.b64encode(userdata_script.encode("utf-8")).decode("utf-8")
    }
)

print(f"✅ Launch Template created with ID: {response['LaunchTemplate']['LaunchTemplateId']}")
