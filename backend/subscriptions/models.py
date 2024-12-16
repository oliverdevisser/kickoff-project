from django.db import models
from django.conf import settings  # Import settings for AUTH_USER_MODEL

class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Dynamically reference the custom user model
        on_delete=models.CASCADE
    )
    stripe_subscription_id = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)