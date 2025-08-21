import boto3

ec2 = boto3.client("ec2", region_name="ap-south-1")
elbv2 = boto3.client("elbv2", region_name="ap-south-1")

vpc_id = "vpc-0fb53498d4739186b"  # from Step 5 infra
hello_tg_arn = "arn:aws:elasticloadbalancing:ap-south-1:388779989161:targetgroup/hello-service-tg/cf5e1176a376553a"
profile_tg_arn = "arn:aws:elasticloadbalancing:ap-south-1:388779989161:targetgroup/profile-service-tg/51bc5a23c6825f88"

# 🔹 1. Auto-discover subnets (pick 2 different AZs)
subnets = ec2.describe_subnets(Filters=[{"Name": "vpc-id", "Values": [vpc_id]}])["Subnets"]
az_map = {}
for subnet in subnets:
    az = subnet["AvailabilityZone"]
    if az not in az_map:
        az_map[az] = subnet["SubnetId"]
chosen_subnets = list(az_map.values())[:2]

if len(chosen_subnets) < 2:
    raise Exception("❌ Need at least 2 subnets in different AZs.")

print(f"✅ Using subnets: {chosen_subnets}")

# 🔹 2. Create new ALB Security Group
sg_response = ec2.create_security_group(
    GroupName="alb-sg",
    Description="Security group for ALB",
    VpcId=vpc_id
)
alb_sg_id = sg_response["GroupId"]

# Allow inbound HTTP (80)
ec2.authorize_security_group_ingress(
    GroupId=alb_sg_id,
    IpPermissions=[{
        "IpProtocol": "tcp",
        "FromPort": 80,
        "ToPort": 80,
        "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
    }]
)

print(f"✅ Created ALB SG: {alb_sg_id}")

# 🔹 3. Create Application Load Balancer
response = elbv2.create_load_balancer(
    Name="backend-alb",
    Subnets=chosen_subnets,
    SecurityGroups=[alb_sg_id],
    Scheme="internet-facing",
    Type="application",
    IpAddressType="ipv4"
)

alb_arn = response["LoadBalancers"][0]["LoadBalancerArn"]
dns_name = response["LoadBalancers"][0]["DNSName"]

print(f"✅ ALB created: {alb_arn}")
print(f"🌍 Access ALB via: http://{dns_name}")

# 🔹 4. Create Listener on Port 80 (default → hello-service)
listener = elbv2.create_listener(
    LoadBalancerArn=alb_arn,
    Protocol="HTTP",
    Port=80,
    DefaultActions=[{"Type": "forward", "TargetGroupArn": hello_tg_arn}]
)
listener_arn = listener["Listeners"][0]["ListenerArn"]

print(f"✅ Listener created on port 80")

# 🔹 5. Add Path Rule for /profile/*
elbv2.create_rule(
    ListenerArn=listener_arn,
    Priority=10,
    Conditions=[{"Field": "path-pattern", "Values": ["/profile/*"]}],
    Actions=[{"Type": "forward", "TargetGroupArn": profile_tg_arn}]
)

print("✅ Rule added: /profile/* → profile-service")
print("✅ Default route: / → hello-service")
