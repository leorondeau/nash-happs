from django.db import models

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE)
    band = models.ForeignKey('Band', on_delete=models.CASCADE)
    time = models.TimeField()
    creator = models.ForeignKey('Creator', on_delete=models.CASCADE, null=True, blank=True)