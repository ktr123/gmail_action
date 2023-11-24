from django.db import models

class emails_data(models.Model):
    message_id = models.CharField(max_length=200)
    from_address = models.TextField()
    subject = models.TextField()
    received_date = models.DateField('date published', blank=True, null=True)

    def __str__(self):
        return self.subject
