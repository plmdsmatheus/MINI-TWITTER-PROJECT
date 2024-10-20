from django.db import models
from users.models import CustomUser

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to="posts_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "post"]

    def __str__(self):
        return f"{self.user} likeed post {self.post.id}"