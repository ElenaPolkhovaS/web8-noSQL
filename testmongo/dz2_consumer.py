import pika
from dz2_contact_model import Contact
from mongoengine import connect

connect(db="homework8_2", host="mongodb://localhost:27017")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='emails')

def send_email_and_update_contact(contact_id):
    print(f"Email sent to contact with ID: {contact_id}")
    
    contact = Contact.objects.get(id=contact_id)
    contact.is_sent = True
    contact.save()

def callback(ch, method, properties, body):
    contact_id = body.decode()
    send_email_and_update_contact(contact_id)

channel.basic_consume(queue='emails', on_message_callback=callback, auto_ack=True)

print('Waiting for messages...')
channel.start_consuming()
