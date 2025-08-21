import boto3

# Initialize EC2 client
ec2 = boto3.client('ec2', region_name='ap-south-1')

# Create Security Group
response = ec2.create_security_group(
    GroupName='backend-sg',
    Description='Security group for backend services',
    VpcId='vpc-0fb53498d4739186b'   # <-- Replace with VPC ID from step5_infra.py
)

sg_id = response['GroupId']
print(f"✅ Created Security Group with ID: {sg_id}")

# Add inbound rules
ec2.authorize_security_group_ingress(
    GroupId=sg_id,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '3.109.208.125/32'}]   # <-- Replace with your IP
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 5000,
            'ToPort': 5000,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 5001,
            'ToPort': 5001,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]
)

print("✅ Inbound rules added successfully!")
