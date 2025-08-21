import boto3

# Replace with your details
hosted_zone_id = "/hostedzone/Z0296136S9QR13WIZLSC"  # Your Route 53 Hosted Zone ID
domain_name = "hello.world."      # Your custom domain
alb_dns_name = "backend-alb-1722893584.ap-south-1.elb.amazonaws.com"  # from load_balancer.py

route53 = boto3.client("route53", region_name="ap-south-1")

# Create or update an Alias record pointing domain → ALB
response = route53.change_resource_record_sets(
    HostedZoneId=hosted_zone_id,
    ChangeBatch={
        "Comment": "Point domain to ALB",
        "Changes": [
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": domain_name,
                    "Type": "A",
                    "AliasTarget": {
                        "HostedZoneId": "ZP97RAFLXTNZK",  # Fixed ELB Hosted Zone ID for ap-south-1
                        "DNSName": alb_dns_name,
                        "EvaluateTargetHealth": False
                    }
                }
            }
        ]
    }
)

print(f"✅ Route53 record created: http://{domain_name}")
