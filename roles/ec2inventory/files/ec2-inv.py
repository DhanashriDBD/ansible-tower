#!/usr/bin/python
import boto3
import csv

# AWS connection with Boto
ec2_cli = boto3.client('ec2',region_name='us-east-2')
all_regions = ec2_cli.describe_regions()
#print(all_regions['Regions'])

#CSV creation and write data to CSV
csv_ob=open("/home/centos/inventory/EC2-Inventory.csv","w",newline='')
csv_w=csv.writer(csv_ob)
csv_w.writerow(['Instance ID','Region','Instance Type','State','Private IP','Public IP','Vpc ID','Subnet ID','Account ID'])

#Fetching AWS regional list from AWS
list_regions = []
for each_reg in all_regions['Regions']:
    #print(each_reg['RegionName'])
    list_regions.append(each_reg['RegionName'])
#print(list_regions)

count=1
for each_reg in list_regions:
    ec2_cli = boto3.client('ec2',region_name=each_reg)
    response=ec2_cli.describe_instances()['Reservations']
    for each_item in response:
        for instances in each_item['Instances']:
            if instances['State']['Name']== 'running' and instances['PublicIpAddress'] != None:
                csv_w.writerow([instances['InstanceId'],instances['Placement']['AvailabilityZone'],
                instances['InstanceType'],instances['State']['Name'],instances['PrivateIpAddress'],instances['PublicIpAddress'],
                instances['VpcId'],instances['SubnetId'],each_item['OwnerId']])
            else:
                instances['PublicIpAddress'] = 'NA'
                publicip= instances['PublicIpAddress']
                csv_w.writerow([instances['InstanceId'],instances['Placement']['AvailabilityZone'],
                instances['InstanceType'],instances['State']['Name'],instances['PrivateIpAddress'],
                publicip,instances['VpcId'],instances['SubnetId'],each_item['OwnerId']])
csv_ob.close()
