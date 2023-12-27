from faker import Faker
from models import Contact
import pika

fake = Faker()

# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue named 'contacts'
channel.queue_declare(queue='contacts')

# Generate fake contacts and publish messages to the 'contacts' queue
for _ in range(5):  # Generate 5 fake contacts
    contact_data = {
        "fullname": fake.name(),
        "email": fake.email(),
        "message_sent": False  # Set to False by default
        # Add other fields as needed
    }

    # Save the contact to MongoDB
    contact = Contact(**contact_data)
    contact.save()

    # Publish the contact ID to the RabbitMQ queue
    message_body = str(contact.id)
    channel.basic_publish(exchange='', routing_key='contacts', body=message_body)

print("Contacts generated and messages published to the 'contacts' queue.")

# Close RabbitMQ connection
connection.close()
