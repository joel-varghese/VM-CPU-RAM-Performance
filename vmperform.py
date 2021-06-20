import paramiko
import os
import pandas as pd
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

host = "192.168.43.157"

def sendcsv():
	mail_content = '''Hello,
	This is a test mail.
	In this mail we are sending some attachments.
	The mail is sent using Python SMTP library as result of vm cpu ram 	   performance.
	Thank You
	'''
	#The mail addresses and password
	sender_address = 'stan3mick@gmail.com'
	sender_pass = 'stan789*'
	receiver_address = 'joelvar17@gmail.com'
	#Setup the MIME
	message = MIMEMultipart()
	message['From'] = sender_address
	message['To'] = receiver_address
	message['Subject'] = 'A test mail sent by Python. It has an attachment.'
	#The subject line
	#The body and the attachments for the mail
	message.attach(MIMEText(mail_content, 'plain'))
	attach_file_name = '/home/joel/result.csv'
	attach_file = open(attach_file_name, 'rb') # Open the file as binarymode
	payload = MIMEBase('application', 'octate-stream')
	payload.set_payload((attach_file).read())
	encoders.encode_base64(payload) #encode the attachment
	#add payload header with filename
	payload.add_header('Content-Decomposition','attachment',filename=attach_file_name)
	message.attach(payload)
	#Create SMTP session for sending the mail
	session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
	session.starttls() #enable security
	session.login(sender_address, sender_pass) #login with mail_id and 
	text = message.as_string()
	session.sendmail(sender_address, receiver_address, text)
	session.quit()
	print('Mail Sent')
def gencsv():
	user = "joel"
	headerlist=["USER","RAM USAGE%","MEMORY USAGE%","TIMESTAMP"]
	cmd=["top -b -n1 > test.txt","sed 's/ \+/,/g' test.txt > office.csv","sed '1,6d' office.csv > office1.csv","sed -n '2,4p; 5q' office1.csv | cut -d, -f3,10-12 > result.csv","cat result.csv"]
	session = paramiko.SSHClient()
	session.load_system_host_keys()
	session.connect(hostname=host,username=user,password="ubuntu")

	for cm in cmd:
		stdin,stdout,stderr = session.exec_command(cm)
		time.sleep(5)
		print(stdout.read().decode())
		print(stderr.read().decode())
	session.close()

	os.system('scp joel@192.168.43.157:/home/joel/result.csv /home/joel')

	file = pd.read_csv("/home/joel/result.csv")
	print("\nmodified file")
	file.to_csv("/home/joel/result.csv",header=headerlist,index=False)
	file2=pd.read_csv("/home/joel/result.csv")
	print(file2)

if __name__ == "__main__":
	gencsv()
	sendcsv()

