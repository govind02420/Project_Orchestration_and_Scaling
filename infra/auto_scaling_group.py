import boto3

autoscaling = boto3.client('autoscaling', region_name='ap-south-1')

# Replace with your Subnet IDs (from infrastructure.py)
SUBNETS = ["subnet-054b5c49f45a1f595", "subnet-029bf10a43f755240"]

response = autoscaling.create_auto_scaling_group(
    AutoScalingGroupName="backend-asg",
    LaunchTemplate={
        "LaunchTemplateName": "backend-launch-template",
        "Version": "$Latest"
    },
    MinSize=1,
    MaxSize=3,
    DesiredCapacity=1,
    VPCZoneIdentifier=",".join(SUBNETS),
    HealthCheckType="EC2",
    HealthCheckGracePeriod=60
)

print("✅ Auto Scaling Group created successfully!")
