import pika
from models import Contact

# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue named 'contacts'
channel.queue_declare(queue='contacts')

def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')

    # Load the contact from MongoDB using the ID
    contact = Contact.objects(id=contact_id).first()

    if contact:
        # Simulate sending email (placeholder)
        print(f"Sending email to {contact.email}...")

        # Update the 'message_sent' field to True
        contact.message_sent = True
        contact.save()

        print(f"Email sent to {contact.email}.")
    else:
        print(f"Contact with ID {contact_id} not found.")

# Set up the consumer to listen for messages from the 'contacts' queue
channel.basic_consume(queue='contacts', on_message_callback=callback, auto_ack=True)

print("Consumer waiting for messages. To exit, press Ctrl+C")

# Start consuming messages
channel.start_consuming()
