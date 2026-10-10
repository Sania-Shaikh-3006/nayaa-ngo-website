from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import VolunteerApplication, PartnershipInquiry, FundraisingCampaign, NewsletterSubscriber, ContactMessage, Donation

class StyledMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

class RegisterForm(StyledMixin, UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class VolunteerForm(StyledMixin, forms.ModelForm):
    class Meta:
        model = VolunteerApplication
        fields = ("name","email","phone","interests","event","message")

class PartnershipForm(StyledMixin, forms.ModelForm):
    class Meta:
        model = PartnershipInquiry
        fields = ("organization","contact_name","email","phone","proposal")

class FundraisingForm(StyledMixin, forms.ModelForm):
    class Meta:
        model = FundraisingCampaign
        fields = ("name","organizer_email","goal","story")

class NewsletterForm(StyledMixin, forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ("email",)

class ContactForm(StyledMixin, forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name","email","inquiry_type","message")

class DonationForm(StyledMixin, forms.ModelForm):
    class Meta:
        model = Donation
        fields = ("donor_name","email","amount","frequency","program","project","gateway")
