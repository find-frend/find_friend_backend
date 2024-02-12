from django.db import models


class EventMember(models.Model):
    event = models.ForeignKey(Event,
                              on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE)
    is_organizer = models.BooleanField()
