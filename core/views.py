from decimal import Decimal

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    RegisterForm,
    VolunteerForm,
    PartnershipForm,
    FundraisingForm,
    NewsletterForm,
    ContactForm,
    DonationForm,
)

from .models import *


# ============================================================
# HOME PAGE
# ============================================================

def home(request):
    stats = list(
        ImpactStat.objects
        .filter(active=True)
        .order_by("order")
    )

    programs = list(
        Program.objects
        .filter(active=True)[:3]
    )

    stories = list(
        Story.objects
        .filter(verified=True)
        .order_by("-created_at")[:3]
    )

    campaigns = list(
        Campaign.objects
        .filter(active=True)[:3]
    )

    projects = list(
        Project.objects
        .filter(verified=True)
        .order_by("-id")[:3]
    )

    demo_stats = [
        {
            "value": "5,000+",
            "label": "People Reached",
            "description": "Demo project figure",
        },
        {
            "value": "25+",
            "label": "Communities",
            "description": "Demo project figure",
        },
        {
            "value": "40+",
            "label": "Learning & Skill Activities",
            "description": "Demo project figure",
        },
        {
            "value": "15+",
            "label": "Community Initiatives",
            "description": "Demo project figure",
        },
    ]

    demo_programs = [
        {
            "title": "Education & Learning",
            "summary": (
                "Creating learning opportunities that help "
                "children build knowledge, confidence, and "
                "skills for their future."
            ),
        },
        {
            "title": "Healthcare & Wellbeing",
            "summary": (
                "Supporting awareness, wellbeing, and "
                "community initiatives that encourage "
                "healthier lives."
            ),
        },
        {
            "title": "Skills & Livelihoods",
            "summary": (
                "Helping people develop useful skills and "
                "explore pathways towards sustainable "
                "livelihood opportunities."
            ),
        },
    ]

    demo_campaigns = [
        {
            "title": "Every Child Deserves an Opportunity",
            "description": (
                "A Nayaa initiative focused on creating "
                "learning and development opportunities "
                "for children."
            ),
        },
        {
            "title": "Women Creating New Possibilities",
            "description": (
                "Supporting women through confidence, "
                "skills, empowerment, and livelihood "
                "opportunities."
            ),
        },
        {
            "title": "Stronger Communities, Brighter Futures",
            "description": (
                "Encouraging community participation, "
                "collaboration, awareness, and local "
                "development."
            ),
        },
    ]

    context = {
        "stats": stats if stats else demo_stats,
        "programs": programs,
        "stories": stories,
        "campaigns": campaigns,
        "projects": projects,
        "demo_programs": demo_programs,
        "demo_campaigns": demo_campaigns,
    }

    return render(
        request,
        "core/home.html",
        context
    )


# ============================================================
# ABOUT
# ============================================================

def about(request):
    return render(request, "core/about.html")


# ============================================================
# OUR WORK
# ============================================================

def work(request):
    return render(
        request,
        "core/work.html",
        {
            "programs": Program.objects.filter(active=True)
        }
    )


# ============================================================
# NAYAA — INDIVIDUAL AREAS OF WORK
# ============================================================

def education(request):
    return render(request, "core/education.html")


def healthcare(request):
    return render(request, "core/healthcare.html")


def women_empowerment(request):
    return render(request, "core/women_empowerment.html")


def skills_livelihoods(request):
    return render(request, "core/skills_livelihoods.html")


def community_development(request):
    return render(request, "core/community_development.html")


# ============================================================
# PROJECTS
# ============================================================

def projects(request):
    return render(
        request,
        "core/projects.html",
        {
            "projects": Project.objects.filter(verified=True)
        }
    )


def stories(request):
    all_stories = Story.objects.filter(
        verified=True
    ).order_by("-created_at")

    return render(
        request,
        "core/stories.html",
        {"stories": all_stories}
    )


def project_detail(request, slug):
    return render(
        request,
        "core/project_detail.html",
        {
            "project": get_object_or_404(
                Project,
                slug=slug,
                verified=True
            )
        }
    )


# ============================================================
# MEDIA
# ============================================================

def media(request):
    return render(
        request,
        "core/media.html",
        {
            "media": MediaItem.objects
                .filter(verified=True)
                .order_by("-created_at"),

            "press": PressRelease.objects
                .order_by("-date"),

            "electronic": ElectronicMedia.objects
                .order_by("-published_on"),
        }
    )


# ============================================================
# VOLUNTEER
# ============================================================

def volunteer(request):
    form = VolunteerForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Thank you. Your volunteer interest has been received."
        )

        return redirect("volunteer")

    return render(
        request,
        "core/volunteer.html",
        {
            "form": form
        }
    )


# ============================================================
# PARTNER
# ============================================================

def partner(request):
    form = PartnershipForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Your partnership proposal has been received."
        )

        return redirect("partner")

    return render(
        request,
        "core/partner.html",
        {
            "form": form
        }
    )


# ============================================================
# FUNDRAISE
# ============================================================

def fundraise(request):
    form = FundraisingForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Your fundraising request has been submitted for review."
        )

        return redirect("fundraise")

    return render(
        request,
        "core/fundraise.html",
        {
            "form": form
        }
    )


# ============================================================
# CAMPAIGNS
# ============================================================

def campaigns(request):
    return render(
        request,
        "core/campaigns.html",
        {
            "campaigns": Campaign.objects.filter(active=True)
        }
    )


# ============================================================
# COMMUNITY
# ============================================================

def community(request):
    form = NewsletterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "You have joined the community newsletter."
        )

        return redirect("community")

    return render(
        request,
        "core/community.html",
        {
            "form": form,
            "events": Event.objects.order_by("date")
        }
    )


# ============================================================
# CONTACT
# ============================================================

def contact(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        obj = form.save()

        send_mail(
            "NGO website inquiry",
            obj.message,
            obj.email,
            ["admin@example.org"],
            fail_silently=True
        )

        messages.success(
            request,
            "Your message has been submitted."
        )

        return redirect("contact")

    return render(
        request,
        "core/contact.html",
        {
            "form": form
        }
    )


# ============================================================
# BLOG
# ============================================================

def blog(request):
    return render(
        request,
        "core/blog.html",
        {
            "posts": BlogPost.objects
                .filter(published=True)
                .order_by("-published_at")
        }
    )


def blog_detail(request, slug):
    return render(
        request,
        "core/blog_detail.html",
        {
            "post": get_object_or_404(
                BlogPost,
                slug=slug,
                published=True
            )
        }
    )


# ============================================================
# DONATE
# ============================================================

def donate(request):
    form = DonationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        donation = form.save()

        messages.info(
            request,
            "Donation record created. Configure Razorpay, "
            "Stripe, or PayPal credentials to start checkout."
        )

        return redirect(
            "donation_thanks",
            pk=donation.pk
        )

    return render(
        request,
        "core/donate.html",
        {
            "form": form
        }
    )


def donation_thanks(request, pk):
    donation = get_object_or_404(
        Donation,
        pk=pk
    )

    return render(
        request,
        "core/donation_thanks.html",
        {
            "donation": donation
        }
    )


# ============================================================
# REGISTER
# ============================================================

def register(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()

        login(
            request,
            user
        )

        return redirect("dashboard")

    return render(
        request,
        "registration/register.html",
        {
            "form": form
        }
    )


# ============================================================
# DASHBOARD SECURITY
# ============================================================

def is_superuser(user):
    return user.is_authenticated and user.is_superuser


# ============================================================
# DASHBOARD
# Only superusers can access this page.
# Contact message count has been removed.
# ============================================================

@user_passes_test(is_superuser, login_url="/admin/login/")
def dashboard(request):

    context = {
        "project_count": Project.objects.count(),

        "volunteer_count": VolunteerApplication.objects.count(),

        "donation_total": (
            Donation.objects
            .filter(status="paid")
            .aggregate(total=Sum("amount"))["total"]
            or Decimal("0")
        ),

        "recent_donations": (
            Donation.objects
            .order_by("-created_at")[:5]
        ),
    }

    return render(
        request,
        "core/dashboard.html",
        context
    )
    # ============================================================
# NAYAA REST API
# ============================================================

@api_view(["GET"])
def api_home(request):
    return Response({
        "organization": "Nayaa",
        "tagline": "For Futures Still Unwritten",
        "message": "Welcome to the Nayaa REST API",
        "available_endpoints": [
            "/api/",
            "/api/programs/",
            "/api/donations/",
            "/api/volunteers/",
        ],
    })
    