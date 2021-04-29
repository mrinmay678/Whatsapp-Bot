from django.db import models

class CSVFile(models.Model):
    file_name = models.FileField(upload_to='phone_csv')
    used = models.BooleanField(default=False)

    def __str__(self):
        return "file"+str(self.id)

class Contact(models.Model):
    phone = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    file_send = models.CharField(
        blank=True, max_length=255)
    time = models.CharField(max_length=15, default='00:00 AM')
    error = models.TextField(blank=True)
    read_status = models.CharField(max_length=20, blank=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return str(self.phone)