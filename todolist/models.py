from django.db import models
from django.urls import reverse


class toDoList(models.Model):
    title = models.CharField(max_length=255, verbose_name="Header")
    content = models.TextField(blank=True, verbose_name="Content")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Photo")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time of creation")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Update time")
    is_published = models.BooleanField(default=True, verbose_name="On portal")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null= True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = "Well know actors"
        verbose_name_plural = "Well know actors"
        ordering = ['time_create', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})
    class Meta:
        verbose_name = "Categories"
        verbose_name_plural = "Categories"
        ordering = ['id', 'name']