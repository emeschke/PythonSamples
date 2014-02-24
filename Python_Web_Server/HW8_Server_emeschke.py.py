#Packages to load
from bottle import route, run, template, get, post, request
import boto.sdb
import boto.sns
import string
from config import *
import time
from boto.sqs.connection import *

#Establish the connection to the simpleDB and SNS.
conn  = boto.sdb.connect_to_region('us-west-2', aws_access_key_id = aws_access_key, aws_secret_access_key = aws_secret_key)
conn1 = boto.sns.SNSConnection(aws_access_key, aws_secret_key)
##********Also establish a connection to SQS and get the queue Emeschke
connSQS = SQSConnection(aws_access_key, aws_secret_key)
domain = "Homework7"
conn.create_domain(domain)
dom = conn.get_domain(domain)
qSQS = connSQS.get_queue('Emeschke')



#Displays an index page with a list of all the items in the domain.
@route('/')
def index():
    result = ''
    for item in dom:
        print item
        result += template('<b> {{name}}</br>', name=item)
    return result + '''<br>Other pages that work:</br>
                        <br>/sns<br>/enter_name<br>'''

#A function that gets/prints all the topics and publishes a form with inputs
#for the topic, protocol and info. 
@route('/sns')
def sns_form():
    sns = conn1.get_all_topics()
    result  = template('<b> {{name}}</br>', name=sns)
    return result+'''<form method="POST" action="/sns">
                <input name="topic" type="text" />
                <input name="protocol" type="text" />
                <input name="info" type="text" />
                <input type="submit" />
                </form><r> Print topic in box1,
                email/url protocol in box2, address in box3</br>'''

#A function that gets the inputs and tries to subscribe to the topic.
#If it works then it confirms, otherwise it goes to an error page (not the if)
#Not sure why the if statement doesn't work correctly.

@route('/sns', method='POST')
def sns_submit():
    topic = request.forms.get('topic')
    protocol = request.forms.get('protocol')
    info = request.forms.get('info')
    if conn1.subscribe(topic, protocol, info) == None:
        return '<b>Did not work, not a valid input.</b>!'
    return template('<b>Entered {{a}} {{b}}</b>!', a=topic, b=info)

#Defines a form where a user can enter the first and last of a new contact

@route('/enter_name')
def name_form():
    return '''<form method="POST" action="/enter_name">
            <input name="first_name" type="text" />
            <input name="last_name" type="text" />
            <input type="submit" />
            </form><r> Print first_name in box1,
            last_name in box2'''

#Str_length is a function that parses the input into a length 16 string,
#letters padded with blank spaces.
#Gets the form info from the above function, assigns a timestamp as a key
#Formats the item in a list and enters it into simpleDB, then notifies the SNS
'''
@route('/enter_name', method='POST')
def str_length(var, length):
    if len(var) > length:
        return var[0:length]
    for i in xrange(len(var)):
        if var[i].isalpha() == False:
            return var[0:i] + " "*(length-i)
    return var + " "*(length - len(var))
'''

@route('/enter_name', method='POST')
def name_submit():
    #get the names from the form
    first_name = request.forms.get('first_name')
    if len(first_name) > 16:
        first_name = first_name[0:16]
    elif first_name.isalpha() == False:
        for i in xrange(len(first_name)):
            if first_name[i].isalpha() == False:
                first_name = first_name[0:i] + " "*(16-i)
    else:
        first_name = first_name + " "*(16 - len(first_name))
    
    last_name = request.forms.get('last_name')
    if len(last_name) > 16:
        last_name = last_name[0:16]
    elif last_name.isalpha() == False:
        for i in xrange(len(last_name)):
            if last_name[i].isalpha() == False:
                last_name = last_name[0:i] + " "*(16-i)
    else:
        last_name = last_name + " "*(16 - len(last_name))
    
    #Assign a timestamp as a unique item key
    item_name = str(time.time())
    item_name = item_name[0:10]
    #collect the item attributes
    item_attrs = {}
    item_attrs['first_name'] = first_name
    item_attrs['last_name'] = last_name
    #Put the list into the simpleDB and publish a notification
    dom.put_attributes(item_name, item_attrs)
    #***********Publish the message into the queue
    m = Message()
    string = item_name+first_name+last_name
    m.set_body(string)
    status = qSQS.write(m)
    #Return a template that shows what was entered.
    return template('<b>Entered {{a}} {{b}}</b>!', a=first_name, b=last_name)

#run(host='localhost', port=8080)

run(host='0.0.0.0', port=8080)
