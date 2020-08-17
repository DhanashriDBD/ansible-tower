import boto3
import csv

# AWS connection with Boto
session     = boto3.Session(profile_name='default', region_name='us-east-2')
client      = session.client(service_name='ec2')
all_regions = client.describe_regions()
#print(all_regions['Regions'])

#CSV creation and write data to CSV
csv_ob=open("/etc/ansible/447721165257/447721165257/roles/vpcsubinventory/files/VPC-Inventory.csv","w",newline='')
csv_w=csv.writer(csv_ob)
csv_w.writerow(['VPC ID','VPC CIDR','Region','VPC State','Subnet','Subnet CIDR','Availability Zone','Owner ID'])

#Fetching AWS regional list from AWS
list_regions = []
for each_reg in all_regions['Regions']:
    #print(each_reg['RegionName'])
    list_regions.append(each_reg['RegionName'])
#print(list_regions)

for each_reg in list_regions:
    connection=boto3.session.Session(profile_name='default',region_name=each_reg)
    ec2_cli=connection.client('ec2')
    response=ec2_cli.describe_vpcs()
    resonse1=ec2_cli.describe_subnets()
    for vpc in response["Vpcs"]:
        for subnet in resonse1["Subnets"]:
             csv_w.writerow([vpc["VpcId"], vpc["CidrBlock"], each_reg, vpc["State"], subnet["SubnetId"],subnet["CidrBlock"], 
             subnet['AvailabilityZone'],vpc["OwnerId"]
             ])
csv_ob.close()
