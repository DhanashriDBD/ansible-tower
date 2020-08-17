import boto3
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

client = boto3.client(
    'ses',
    region_name='us-east-2'
)

message = MIMEMultipart()
message['Subject'] = 'VPC Dynamic Inventory is updated'
message['From'] = 'dhanashree.dbfree@gmail.com'
message['To'] = ', '.join(['dhanashree.dbfree@gmail.com','dhanashree.dhamgunde@zensar.com'])

#message body
part = MIMEText('Dear Receiver, this is to inform you that AWS VPC inventory has been updated.Please find attached updated inventory', 'html')
message.attach(part)
attachment_string = ''
# attachment
if attachment_string:   # if bytestring available
    part = MIMEApplication(str.encode('attachment_string'))
else:
    part = MIMEApplication(open('/etc/ansible/447721165257/447721165257/roles/vpcsubinventory/files/VPC-Inventory.csv', 'rb').read())
    print(part)
part.add_header('Content-Disposition', 'attachment', filename='VPC-Inventory.csv')
message.attach(part)
response = client.send_raw_email(
    Source=message['From'],
    Destinations=['dhanashree.dbfree@gmail.com','dhanashree.dhamgunde@zensar.com'],
    RawMessage={
        'Data': message.as_string()
    }
)

