from django.db import models
from users.models import CustomUser

class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="following")
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["follower", "following"]

    def __str__(self):
        return f"{self.follower} follows {self.following}"