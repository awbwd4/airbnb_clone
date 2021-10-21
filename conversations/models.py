from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from core import models as core_models


class Conversation(core_models.TimeStampModel):

    """Conversation Model Definition"""

    participants = models.ManyToManyField("users.User", blank=True)

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)
        return " - ".join(usernames)

    def count_messages(self):
        return self.messages.count()

    def count_participants(self):
        return self.participants.count()

    count_messages.short_description = "Number Of Messages"
    count_participants.short_description = "Number Of Participants"


class Message(core_models.TimeStampModel):

    message = models.TextField()
    user = ForeignKey("users.User", related_name="messages", on_delete=models.CASCADE)
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=CASCADE
    )

    def __str__(self):
        return f"{self.user} says : {self.message}"
