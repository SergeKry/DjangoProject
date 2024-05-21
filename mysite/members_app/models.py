from django.db import models


class Input(models.Model):
    member_input = models.TextField()

    def __str__(self):
        return self.member_input
