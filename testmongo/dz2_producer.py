import pika
from faker import Faker
from mongoengine import connect, Document, StringField, BooleanField
from dz2_contact_model import Contact

connect(db="homework8_2", host="mongodb://localhost:27017")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='emails')

def send_message(contact_id):
    channel.basic_publish(exchange='',
                          routing_key='emails',
                          body=str(contact_id))

def produce_contacts(num_contacts):
    fake = Faker()
    for _ in range(num_contacts):
        full_name = fake.name()
        email = fake.email()
        contact = Contact(full_name=full_name, email=email)
        contact.save()
        send_message(contact.id)

if __name__ == "__main__":
    num_contacts = 10
    produce_contacts(num_contacts)
    print(f"{num_contacts} contacts generated and placed in the queue.")
