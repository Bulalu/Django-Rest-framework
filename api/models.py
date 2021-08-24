from django.db import models


class Club(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    club = models.CharField(max_length=50)
    position = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name
