from django.db import models


class Contact(models.Model):
    """Model for contact form"""
    CONTACT_CHOICES = [
        ('order', 'Order Tracking'),
        ('general', 'General Query'),
        ('complaint', 'Complaint'),
        ('return', 'Return Request'),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    reason = models.CharField(max_length=15, choices=CONTACT_CHOICES)
    message = models.TextField(max_length=700)

    def __str__(self):
        return self.email
