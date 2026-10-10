from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("our-work/", views.work, name="work"),
    # Individual areas of work
    path("education/", views.education, name="education"),
    path("healthcare/", views.healthcare, name="healthcare"),
    path("women-empowerment/", views.women_empowerment, name="women_empowerment"),
    path("skills-livelihoods/", views.skills_livelihoods, name="skills_livelihoods"),
    path("community-development/", views.community_development, name="community_development"),
    path("projects/", views.projects, name="projects"),
    path("stories/", views.stories, name="stories"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("media/", views.media, name="media"),
    path("get-involved/volunteer/", views.volunteer, name="volunteer"),
    path("get-involved/partner/", views.partner, name="partner"),
    path("get-involved/fundraise/", views.fundraise, name="fundraise"),
    path("get-involved/campaigns/", views.campaigns, name="campaigns"),
    path("get-involved/community/", views.community, name="community"),
    path("blog/", views.blog, name="blog"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("contact/", views.contact, name="contact"),
    path("donate/", views.donate, name="donate"),
    path("donate/thanks/<int:pk>/", views.donation_thanks, name="donation_thanks"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("forgot-password/", auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"), name="password_reset"),
    path(
    "forgot-password/",
    auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset_form.html"
    ),
    name="forgot_password",
),

path(
    "forgot-password/done/",
    auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"
    ),
    name="password_reset_done",
),

path(
    "reset/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html"
    ),
    name="password_reset_confirm",
),

path(
    "reset/done/",
    auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"
    ),
    name="password_reset_complete",
),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("api/", views.api_home, name="api_home"),

]
