from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class ImpactStat(models.Model):
    label = models.CharField(max_length=120)
    value = models.CharField(max_length=40)
    description = models.CharField(max_length=180, blank=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.value} – {self.label}"


class Story(models.Model):
    title = models.CharField(max_length=180)
    summary = models.TextField()
    image = models.ImageField(upload_to="stories/", blank=True, null=True)
    verified = models.BooleanField(
        default=False,
        help_text="Publish only when the story and image are verified."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


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

    def __str__(self):
        return self.title


class Campaign(models.Model):
    title = models.CharField(max_length=180)
    summary = models.TextField()
    details = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


# ✅ PASTE THIS NEW CODE IN ITS PLACE:
class Project(models.Model):
    STATUS_CHOICES = [
        ("Ongoing", "Ongoing"),
        ("Completed", "Completed"),
        ("Upcoming", "Upcoming"),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Ongoing")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    sector = models.CharField(max_length=80, blank=True)
    goals = models.TextField(blank=True)
    beneficiaries = models.TextField(blank=True)
    timeline = models.CharField(max_length=180, blank=True)
    cover_image = models.ImageField(upload_to="projects/", blank=True, null=True)
    report = models.FileField(upload_to="reports/", blank=True, null=True)
    verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "projects"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "project"
            slug = base_slug
            count = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("project_detail", args=[self.slug])

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    """Table: project_images (from PDF 4)"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="project_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "project_images"

    def __str__(self):
        return f"Image for {self.project.title}"

    @property
    def image_url(self):
        return self.image.url if self.image else ""

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="project_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "project_images"

    def __str__(self):
        return f"Image for {self.project.title}"

    @property
    def image_url(self):
        return self.image.url if self.image else ""
class MediaItem(models.Model):
    TYPE = [
        ("photo", "Photo"),
        ("video", "Video"),
    ]

    title = models.CharField(max_length=180)
    media_type = models.CharField(max_length=20, choices=TYPE)
    image = models.ImageField(upload_to="media/", blank=True, null=True)
    video_url = models.URLField(blank=True)
    caption = models.CharField(max_length=240, blank=True)
    source_credit = models.CharField(max_length=240, blank=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PressRelease(models.Model):
    title = models.CharField(max_length=220)
    date = models.DateField()
    body = models.TextField()
    source_url = models.URLField(blank=True)

    def __str__(self):
        return self.title


class ElectronicMedia(models.Model):
    outlet = models.CharField(max_length=160)
    title = models.CharField(max_length=220)
    url = models.URLField()
    published_on = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.outlet}: {self.title}"


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
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog_detail", args=[self.slug])

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=180)
    date = models.DateField()
    location = models.CharField(max_length=180)
    description = models.TextField()
    registration_url = models.URLField(blank=True)

    def __str__(self):
        return self.title


class VolunteerApplication(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    interests = models.CharField(max_length=250)
    message = models.TextField(blank=True)
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PartnershipInquiry(models.Model):
    organization = models.CharField(max_length=180)
    contact_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    proposal = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.organization

# NEW: CONFIRMED PARTNERS AND SUPPORTERS
class Partner(models.Model):
    name = models.CharField(max_length=180)
    logo = models.ImageField(
        upload_to="partners/",
        blank=True,
        null=True
    )
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class FundraisingCampaign(models.Model):
    name = models.CharField(max_length=180)
    organizer_email = models.EmailField()
    goal = models.DecimalField(max_digits=12, decimal_places=2)
    story = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default="pending review")

    def __str__(self):
        return self.name


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class ContactMessage(models.Model):
    INQUIRY = [
        ("general", "General"),
        ("media", "Media"),
        ("partnership", "Partnership"),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    inquiry_type = models.CharField(max_length=30, choices=INQUIRY, default="general")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} – {self.inquiry_type}"


class Donation(models.Model):
    FREQUENCY = [
        ("one_time", "One-time"),
        ("recurring", "Recurring"),
    ]
    STATUS = [
        ("created", "Created"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]

    donor_name = models.CharField(max_length=150)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    frequency = models.CharField(max_length=20, choices=FREQUENCY, default="one_time")
    program = models.ForeignKey(
        Program,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    gateway = models.CharField(max_length=30, default="razorpay")
    gateway_order_id = models.CharField(max_length=120, blank=True)
    gateway_payment_id = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="created")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor_name} – ₹{self.amount}"


class BannerSlide(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="banners/")
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class HomePageContent(models.Model):
    vision_title = models.CharField(max_length=200, default="Our Vision")
    vision_description = models.TextField()
    mission_title = models.CharField(max_length=200, default="Our Mission")
    mission_description = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Nayaa Homepage Content"
        # ============================================================
# ABOUT US DYNAMIC MODELS (From PDF 3)
# ============================================================

class OurStory(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "our_story"
        verbose_name = "Our Story"
        verbose_name_plural = "Our Story"

    def __str__(self):
        return f"Story ({self.created_at.strftime('%Y-%m-%d')})"


class CoreValue(models.Model):
    value = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "core_values"
        verbose_name = "Core Value"
        verbose_name_plural = "Core Values"

    def __str__(self):
        return self.value


class AboutProgram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "programs"
        verbose_name = "About Program"
        verbose_name_plural = "About Programs"

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    image = models.ImageField(upload_to="team/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "team_members"
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} - {self.role}"
    
    # ============================================================
# MEDIA PAGE MODELS (From PDF 3 Database Design)
# ============================================================

class PressReleaseItem(models.Model):
    """Table 1: press_releases"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "press_releases"
        ordering = ["-release_date"]

    def __str__(self):
        return self.title


class MediaCoverage(models.Model):
    """Table 2: media_coverage"""
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=2083)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "media_coverage"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ImageGallery(models.Model):
    """Table 3: image_gallery"""
    image = models.ImageField(upload_to="gallery/")
    description = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "image_gallery"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.description or f"Gallery Image {self.id}"

    @property
    def image_path(self):
        return self.image.url if self.image else ""


class Video(models.Model):
    """Table 4: videos"""
    video_url = models.URLField(max_length=2083)
    description = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "videos"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.description or self.video_url

    @property
    def embed_url(self):
        url = self.video_url
        if "watch?v=" in url:
            video_id = url.split("watch?v=")[1].split("&")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return url