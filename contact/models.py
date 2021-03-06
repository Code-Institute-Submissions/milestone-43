from django.db import models


class Contact(models.Model):

    class Meta:
        verbose_name_plural = 'Contact'

    name = models.CharField(max_length=50)
    email = models.EmailField()
    message_title = models.CharField(max_length=100)
    message = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return self.name
