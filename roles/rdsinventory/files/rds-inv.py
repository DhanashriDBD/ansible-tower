import boto3
import csv

# AWS connection with Boto
session     = boto3.Session(profile_name='default', region_name='us-east-2')
client      = session.client(service_name='ec2')
all_regions = client.describe_regions()
#print(all_regions['Regions'])

#CSV creation and write data to CSV
csv_ob=open("/etc/ansible/447721165257/447721165257/roles/rdsinventory/files/RDS-Inventory.csv","w",newline='')
csv_w=csv.writer(csv_ob)
csv_w.writerow(['DB Name','DB Engine','Region','Instance Type','State','Endpoint','Vpc ID','Subnet ID'])

#Fetching AWS regional list from AWS
list_regions = []
for each_reg in all_regions['Regions']:
    #print(each_reg['RegionName'])
    list_regions.append(each_reg['RegionName'])
#print(list_regions)

count=1
for each_reg in list_regions:
    connection=boto3.session.Session(profile_name='default',region_name=each_reg)
    rds_cli=connection.client('rds')
    response=rds_cli.describe_db_instances()['DBInstances']
    for each_item in response:
        csv_w.writerow([each_item['DBInstanceIdentifier'],each_item['Engine'],each_item['AvailabilityZone'],
        each_item['DBInstanceClass'],each_item['DBInstanceStatus'], each_item['Endpoint']['Address'],
        each_item['DBSubnetGroup']['VpcId'],each_item['DBSubnetGroup']['DBSubnetGroupName']
        ])
csv_ob.close()
