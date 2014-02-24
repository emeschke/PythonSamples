import boto
from config import *
from boto.sqs.connection import *
import boto.sns

#Messages are setup to be a string of item_name, first_name, last_name. The
#first 10 characters are the item name, the next 16 are the first name, the
#last 16 are the last name.

#Establish connections with SNS, S3 and SQS, create a queue
conn1 = boto.sns.SNSConnection(aws_access_key, aws_secret_key)
s3 = boto.connect_s3(aws_access_key, aws_secret_key)
conn = SQSConnection(aws_access_key, aws_secret_key)
bucket = s3.get_bucket('emeschke')
q = conn.create_queue('Emeschke')

#Get up to 10 messages from the queue and then print how many.

rs = q.get_messages(num_messages = 10)
if len(rs)==0:
    print "There are no messages in the queue."

for i in xrange(len(rs)):
    #Iterate through the different messages from the queue.  And get the items.
    item_name = rs[i].get_body()[0:10]
    first_name = rs[i].get_body()[10:26]
    last_name = rs[i].get_body()[26:42]
    #Create a message to be published to the 51083-updated and send it.
    message = "Added key:" + item_name +"\n"+ first_name +" " + last_name + "\nhttps://s3.amazonaws.com/emeschke/" + item_name + "new.html"
    subject = "Added item"
    conn1.publish('arn:aws:sns:us-east-1:274755131397:51083-updated', message, subject)
    print item_name + ": " + first_name + last_name
    #Create a new contact file and add it to the bucket.
    key = bucket.new_key('{0}new.html'.format(item_name))
    string = '<HTML><HEAD><BODY>'
    string += '<H1>' + "First_name:" + ': ' + first_name + '<H1>'
    string += '<H1>' + "Last_name:" + ': ' + last_name + '<H1>'
    string +='</BODY></HTML>'
    key.set_contents_from_string(string, headers={'Content-Type': 'text/html'})
    q.delete_message(rs[i])

    
