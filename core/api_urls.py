from django.urls import path
from rest_framework.routers import DefaultRouter
from .api import ProjectViewSet, BlogPostViewSet, ImpactStatViewSet, ContactMessageViewSet

router = DefaultRouter()
router.register("projects", ProjectViewSet)
router.register("blogs", BlogPostViewSet)
router.register("impact", ImpactStatViewSet)
router.register("contact", ContactMessageViewSet)

urlpatterns = router.urls
