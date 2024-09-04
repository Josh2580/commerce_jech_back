# products/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Product

@receiver(post_save, sender=Product)
def check_store_creation(sender, instance, created, **kwargs):
    print("Testing Signals")
    print(f"instance: {instance}")
    print(f"sender: {sender.filter.count()}")
    print("End Testing Signals")

    user = instance.store
    if user and created:
        print("Testing Signals Created")
        print(user)
        send_mail(
            'Store Creation Required',
            'Please create a store to list more than 2 products.',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
