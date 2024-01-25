from django.db import models

class Blog(models.Model):

    class Tags(models.TextChoices):
        PYTHON = 'py'
        PHP = 'php'
        LANGAGE = 'lg'
        POLITIQUE = 'pol'
        SPORT = 'sp'


    titre = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, null=True)
    photo = models.CharField(max_length=255, null=True)
    tag=models.CharField(choices=Tags.choices, max_length=10, null=True)
    