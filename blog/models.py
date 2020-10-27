from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete = models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_on = models.DateTimeField(default = timezone.now())
    published_on = models.DateTimeField(blank = True , null = True)
    is_deleted = models.BooleanField(default=False)

    class Meta():
        db_table = 'post'

    def publish(self):
        self.published_on = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comment.filter(approved_comments=True)

    def get_absolute_url(self):
        return reverse('post_detail',kwargs = {'pk':self.pk})

    def delete(self,hard = False):
        if hard:
            super().delete()
        else:
            self.is_deleted = True
            self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post',on_delete = models.CASCADE,related_name='comments')
    author = models.CharField(max_length = 50)
    text = models.TextField()
    created_on = models.DateTimeField(default=timezone.now())
    approved_comments = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def approve(self):
        self.approved_comments = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

    def delete(self,hard = False):
        if hard:
            super().delete()
        else:
            self.is_deleted = True
            self.save()

    def __str__(self):
        return self.text
