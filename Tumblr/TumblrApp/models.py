from django.db import models


class Post(models.Model):
    class PostType(models.TextChoices):
        Blog = "Blog"
        Quote = "Quote"
        Images = "images"
        Image = "Image"
        Video = "Video"
        Github = "Github"
        Bookmark = "Bookmark"

    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=20)
    likes = models.IntegerField()
    tags = models.CharField(max_length=200)
    post_type = models.CharField(choices=PostType.choices, max_length=10, default="text")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0}'s {1}".format(self.user, self.id)


class Text(models.Model):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    text1 = models.CharField(max_length=1000)
    text2 = models.CharField(max_length=2000)

    def __str__(self):
        return "{0}'s {1} post -> {2} with {3}".format(self.user, self.id, self.text1, self.text2)


class Link(models.Model):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    url = models.CharField(max_length=1000)
    caption = models.CharField(max_length=2000)

    def __str__(self):
        return "{0}'s {1} post-> {2} with {3}".format(self.post.user, self.post.id, self.url, self.caption)


class File(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    file = models.FileField(upload_to='images/', )

    def __str__(self):
        return "{0} for {1} post of type File -> name: {2}".format(self.id, self.post, self.file.name)
