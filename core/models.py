from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class ImpactStat(models.Model):
    label = models.CharField(max_length=120)
    value = models.CharField(max_length=40)
    description = models.CharField(max_length=180, blank=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    def __str__(self): return f"{self.value} – {self.label}"

class Story(models.Model):
    title = models.CharField(max_length=180)
    summary = models.TextField()
    image = models.ImageField(upload_to="stories/", blank=True, null=True)
    verified = models.BooleanField(default=False, help_text="Publish only when the story and image are verified.")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class Program(models.Model):
    CATEGORY_CHOICES = [
        ("education", "Education"),
        ("health", "Healthcare"),
        ("livelihood", "Livelihood"),
    ]
    title = models.CharField(max_length=160)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    summary = models.TextField()
    details = models.TextField(blank=True)
    image = models.ImageField(upload_to="programs/", blank=True, null=True)
    active = models.BooleanField(default=True)
    def __str__(self): return self.title

class Campaign(models.Model):
    title = models.CharField(max_length=180)
    summary = models.TextField()
    details = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    def __str__(self): return self.title

class Project(models.Model):
    STATUS = [("ongoing", "Ongoing"), ("completed", "Completed")]
    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True, blank=True)
    sector = models.CharField(max_length=80)
    goals = models.TextField()
    beneficiaries = models.TextField()
    timeline = models.CharField(max_length=180)
    location = models.CharField(max_length=180)
    description = models.TextField()
    cover_image = models.ImageField(upload_to="projects/", blank=True, null=True)
    report = models.FileField(upload_to="reports/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default="ongoing")
    verified = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def get_absolute_url(self): return reverse("project_detail", args=[self.slug])
    def __str__(self): return self.title

class MediaItem(models.Model):
    TYPE = [("photo", "Photo"), ("video", "Video")]
    title = models.CharField(max_length=180)
    media_type = models.CharField(max_length=20, choices=TYPE)
    image = models.ImageField(upload_to="media/", blank=True, null=True)
    video_url = models.URLField(blank=True)
    caption = models.CharField(max_length=240, blank=True)
    source_credit = models.CharField(max_length=240, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class PressRelease(models.Model):
    title = models.CharField(max_length=220)
    date = models.DateField()
    body = models.TextField()
    source_url = models.URLField(blank=True)
    def __str__(self): return self.title

class ElectronicMedia(models.Model):
    outlet = models.CharField(max_length=160)
    title = models.CharField(max_length=220)
    url = models.URLField()
    published_on = models.DateField(null=True, blank=True)
    def __str__(self): return f"{self.outlet}: {self.title}"

class BlogPost(models.Model):
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=100, blank=True)
    excerpt = models.TextField()
    body = models.TextField()
    image = models.ImageField(upload_to="blog/", blank=True, null=True)
    published_at = models.DateTimeField()
    published = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def get_absolute_url(self): return reverse("blog_detail", args=[self.slug])
    def __str__(self): return self.title

class Event(models.Model):
    title = models.CharField(max_length=180)
    date = models.DateField()
    location = models.CharField(max_length=180)
    description = models.TextField()
    registration_url = models.URLField(blank=True)
    def __str__(self): return self.title

class VolunteerApplication(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    interests = models.CharField(max_length=250)
    message = models.TextField(blank=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class PartnershipInquiry(models.Model):
    organization = models.CharField(max_length=180)
    contact_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    proposal = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.organization

class FundraisingCampaign(models.Model):
    name = models.CharField(max_length=180)
    organizer_email = models.EmailField()
    goal = models.DecimalField(max_digits=12, decimal_places=2)
    story = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default="pending review")
    def __str__(self): return self.name

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    def __str__(self): return self.email

class ContactMessage(models.Model):
    INQUIRY = [("general","General"),("media","Media"),("partnership","Partnership")]
    name = models.CharField(max_length=150)
    email = models.EmailField()
    inquiry_type = models.CharField(max_length=30, choices=INQUIRY, default="general")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.name} – {self.inquiry_type}"

class Donation(models.Model):
    FREQUENCY = [("one_time","One-time"),("recurring","Recurring")]
    STATUS = [("created","Created"),("paid","Paid"),("failed","Failed")]
    donor_name = models.CharField(max_length=150)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    frequency = models.CharField(max_length=20, choices=FREQUENCY, default="one_time")
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    gateway = models.CharField(max_length=30, default="razorpay")
    gateway_order_id = models.CharField(max_length=120, blank=True)
    gateway_payment_id = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="created")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.donor_name} – ₹{self.amount}"
