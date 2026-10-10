# NGO CMS – Django/Python

This project is a full Django/Python NGO CMS starter based on the supplied internship requirements.

## Included modules

- Home: mission, vision, programs, impact statistics, stories and campaigns
- About Us: mission, vision and history
- Our Work: education, healthcare and livelihood programs
- Projects: ongoing/completed projects, goals, beneficiaries, timeline, location, reports and media
- Media: photos/videos, press releases and electronic media
- Get Involved: volunteer, partner, fundraise, campaigns, community/newsletter and donate
- Blog: project updates, success stories, interviews and social-issue articles
- Contact: inquiry form, contact details and map area
- Donate: one-time/recurring amount selection and project/program selection
- Authentication: registration, login, logout, password reset
- Admin dashboard through Django admin
- REST API for projects, blog posts, impact statistics and form submissions
- MySQL-ready database configuration
- Razorpay integration hook; Stripe/PayPal environment variables are included for later live integration
- Responsive Bootstrap UI
- Accessibility-oriented labels, focus states and semantic structure
- SEO metadata, sitemap and robots.txt
- Multilingual/i18n scaffolding (English/Hindi)
- Media upload through Django admin
- GitHub/deployment instructions

## Important authenticity rule

The requirement asks for real-life photos. This starter uses external stock-photo URLs only as temporary visual placeholders. They are real photographs of people, but they are NOT photographs of a real NGO's beneficiaries or projects. Do not present stock photos as actual field stories.

For a real NGO deployment, upload photographs for which the NGO has permission and add the correct captions, dates, locations and consent information through `/admin/`.

## Run locally

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- Public site: http://127.0.0.1:8000/
- Admin/CMS: http://127.0.0.1:8000/admin/
- API: http://127.0.0.1:8000/api/

For final deployment, configure MySQL, environment secrets, HTTPS, `ALLOWED_HOSTS`, static/media storage, email, payment credentials and a production WSGI/ASGI server.

## Requirement mapping

The project structure intentionally keeps content in database models so non-technical staff can manage content from Django admin. Django's admin, templates, forms, models and static-file system are used for the CMS workflow.

Do not enter made-up impact numbers, project histories, NGO addresses, donor information or success stories. Replace demo records with verified information before publishing.
