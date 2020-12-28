from django.db import models

# Create your models here.


class FileData(models.Model):
    resume_file=models.FileField(upload_to='resumes/')

