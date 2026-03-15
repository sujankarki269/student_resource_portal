from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

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
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='programs', null=True, blank=True)
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
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

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


class PortfolioProfile(models.Model):
    # Basic personal info
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    nationality = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True, choices=[('Male','Male'), ('Female','Female'), ('Other','Other')])
    
    # Profile picture and bio
    profile_picture = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    bio = models.TextField(blank=True, help_text="Short introduction")
    
    # Social links (optional)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)

    class Meta:
        verbose_name = "Portfolio Profile"
        verbose_name_plural = "Portfolio Profile"

    def __str__(self):
        return f"{self.first_name} {self.surname}"

class WorkExperience(models.Model):
    profile = models.ForeignKey(PortfolioProfile, on_delete=models.CASCADE, related_name='work_experiences')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # blank means current
    job_title = models.CharField(max_length=200)
    employer = models.CharField(max_length=200)
    responsibilities = models.TextField(blank=True, help_text="List of responsibilities (one per line)")
    order = models.PositiveIntegerField(default=0, help_text="Display order (ascending)")

    class Meta:
        ordering = ['order', '-start_date']

    def __str__(self):
        return f"{self.job_title} at {self.employer}"

class Education(models.Model):
    profile = models.ForeignKey(PortfolioProfile, on_delete=models.CASCADE, related_name='educations')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    description = models.TextField(blank=True, help_text="Additional details (grade, etc.)")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-start_date']

    def __str__(self):
        return f"{self.degree} at {self.institution}"

class Publication(models.Model):
    profile = models.ForeignKey(PortfolioProfile, on_delete=models.CASCADE, related_name='publications')
    title = models.CharField(max_length=300)
    conference_journal = models.CharField(max_length=300, blank=True)
    date = models.DateField()
    authors = models.CharField(max_length=500, help_text="List authors as they appear")
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-date']

    def __str__(self):
        return self.title

class HonorAward(models.Model):
    profile = models.ForeignKey(PortfolioProfile, on_delete=models.CASCADE, related_name='honors')
    title = models.CharField(max_length=300)
    issuer = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-date']

    def __str__(self):
        return self.title

class SubjectTaught(models.Model):
    profile = models.ForeignKey(PortfolioProfile, on_delete=models.CASCADE, related_name='subjects_taught')
    name = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('technical', 'Technical'),
        ('language', 'Language'),
        ('soft', 'Soft Skills'),
    ]
    profile = models.ForeignKey(PortfolioProfile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='technical')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blog_posts')
    content = RichTextUploadingField(help_text="Write your article with images, etc.")
    summary = models.TextField(blank=True, help_text="Short description for listings")
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    views = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title