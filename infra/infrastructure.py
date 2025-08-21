import boto3

# ---------- CONFIG ----------
REGION = "ap-south-1"
VPC_CIDR = "10.0.0.0/16"
PUBLIC_SUBNET_CIDR = "10.0.1.0/24"
PRIVATE_SUBNET_CIDR = "10.0.2.0/24"
SECURITY_GROUP_NAME = "mern-sg"
SECURITY_GROUP_DESC = "Security group for MERN app"

# ---------- CLIENT ----------
ec2 = boto3.client("ec2", region_name=REGION)

def create_vpc():
    vpc = ec2.create_vpc(CidrBlock=VPC_CIDR)
    vpc_id = vpc["Vpc"]["VpcId"]
    print(f"✅ Created VPC: {vpc_id}")

    # Enable DNS
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={"Value": True})
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={"Value": True})
    return vpc_id

def create_subnet(vpc_id, cidr, public=True):
    subnet = ec2.create_subnet(CidrBlock=cidr, VpcId=vpc_id)
    subnet_id = subnet["Subnet"]["SubnetId"]

    # Auto-assign public IPs for public subnet
    if public:
        ec2.modify_subnet_attribute(SubnetId=subnet_id, MapPublicIpOnLaunch={"Value": True})

    print(f"✅ Created {'Public' if public else 'Private'} Subnet: {subnet_id}")
    return subnet_id

def create_internet_gateway(vpc_id):
    igw = ec2.create_internet_gateway()
    igw_id = igw["InternetGateway"]["InternetGatewayId"]

    ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
    print(f"✅ Attached Internet Gateway: {igw_id}")
    return igw_id

def create_route_table(vpc_id, subnet_id, igw_id):
    rt = ec2.create_route_table(VpcId=vpc_id)
    rt_id = rt["RouteTable"]["RouteTableId"]

    # Add route to internet
    ec2.create_route(
        RouteTableId=rt_id,
        DestinationCidrBlock="0.0.0.0/0",
        GatewayId=igw_id
    )

    # Associate with public subnet
    ec2.associate_route_table(RouteTableId=rt_id, SubnetId=subnet_id)
    print(f"✅ Created & Associated Route Table: {rt_id}")
    return rt_id

def create_security_group(vpc_id):
    sg = ec2.create_security_group(
        GroupName=SECURITY_GROUP_NAME,
        Description=SECURITY_GROUP_DESC,
        VpcId=vpc_id
    )
    sg_id = sg["GroupId"]

    # Allow SSH, HTTP, App traffic
    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22,
             "IpRanges": [{"CidrIp": "0.0.0.0/0"}]},
            {"IpProtocol": "tcp", "FromPort": 80, "ToPort": 80,
             "IpRanges": [{"CidrIp": "0.0.0.0/0"}]},
            {"IpProtocol": "tcp", "FromPort": 3000, "ToPort": 3000,
             "IpRanges": [{"CidrIp": "0.0.0.0/0"}]}
        ]
    )

    print(f"✅ Created Security Group: {sg_id}")
    return sg_id

def main():
    # 1. VPC
    vpc_id = create_vpc()

    # 2. Subnets
    public_subnet_id = create_subnet(vpc_id, PUBLIC_SUBNET_CIDR, public=True)
    private_subnet_id = create_subnet(vpc_id, PRIVATE_SUBNET_CIDR, public=False)

    # 3. IGW
    igw_id = create_internet_gateway(vpc_id)

    # 4. Route Table for public subnet
    rt_id = create_route_table(vpc_id, public_subnet_id, igw_id)

    # 5. Security Group
    sg_id = create_security_group(vpc_id)

    print("\n🚀 Infrastructure Setup Complete!")
    print(f"VPC: {vpc_id}")
    print(f"Public Subnet: {public_subnet_id}")
    print(f"Private Subnet: {private_subnet_id}")
    print(f"Internet Gateway: {igw_id}")
    print(f"Route Table: {rt_id}")
    print(f"Security Group: {sg_id}")

if __name__ == "__main__":
    main()
