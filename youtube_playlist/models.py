from django.db import models


class Tags(models.Model):
    tag = models.CharField(max_length=100)
    count = models.PositiveIntegerField(default=1)
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE, related_name="tags")

    def __str__(self):
        return self.tag
