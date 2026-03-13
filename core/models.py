from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True)
    semester = models.IntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Note(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    file = models.FileField(upload_to='notes/')
    description = models.TextField(blank=True)
    upload_date = models.DateTimeField(default=timezone.now)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    downloads = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

class Assignment(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    ]
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    file = models.FileField(upload_to='assignments/', blank=True, null=True)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    upload_date = models.DateTimeField(default=timezone.now)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    downloads = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

class Program(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    code_snippet = models.TextField(help_text="Paste code here")
    language = models.CharField(max_length=50, default='python')
    file = models.FileField(upload_to='programs/', blank=True, null=True)
    upload_date = models.DateTimeField(default=timezone.now)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    downloads = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, help_text="Optional description of the category")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Tutorial(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='tutorials')
    content = models.TextField(help_text="Write tutorial content here")
    video_link = models.URLField(blank=True, help_text="YouTube or Vimeo link")
    file = models.FileField(upload_to='tutorials/', blank=True, null=True)
    upload_date = models.DateTimeField(default=timezone.now)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    downloads = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, help_text="Contact phone number")
    address = models.TextField(blank=True, help_text="Full address")
    # You can add more fields as needed

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # For existing users, ensure profile exists (in case it was missing)
        Profile.objects.get_or_create(user=instance)