from django.contrib import admin
from .models import *

admin.site.site_header = "NGO CMS Administration"
admin.site.site_title = "NGO CMS"
admin.site.index_title = "Content, forms, donations and impact management"

for model in [
    ImpactStat, Story, Program, Campaign, Project, MediaItem, PressRelease,
    ElectronicMedia, BlogPost, Event, VolunteerApplication, PartnershipInquiry,
    FundraisingCampaign, NewsletterSubscriber, ContactMessage, Donation
]:
    admin.site.register(model)
