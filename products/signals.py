# products/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Product

@receiver(post_save, sender=Product)
def check_store_creation(sender, instance, **kwargs):
    user = instance.store.owner
    if not user.stores.exists() and Product.objects.filter(store__owner=user).count() >= 2:
        send_mail(
            'Store Creation Required',
            'Please create a store to list more than 2 products.',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
