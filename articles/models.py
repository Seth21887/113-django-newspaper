from django.db import models
from django.contrib.auth import get_user_model #safe way of representing the user model that is active already on the system.
from django.urls import reverse 


class Section(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return self.name

class ArticleType(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=128)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    _type = models.ForeignKey(
        ArticleType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) #this will auto populate any time we create a new record on this table.
    
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', args=[self.id])