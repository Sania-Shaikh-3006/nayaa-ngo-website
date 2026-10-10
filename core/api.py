from rest_framework import permissions, serializers, viewsets
from .models import Project, BlogPost, ImpactStat, ContactMessage

class ProjectSerializer(serializers.ModelSerializer):
    class Meta: model = Project; fields = "__all__"

class BlogSerializer(serializers.ModelSerializer):
    class Meta: model = BlogPost; fields = "__all__"

class ImpactSerializer(serializers.ModelSerializer):
    class Meta: model = ImpactStat; fields = "__all__"

class ContactSerializer(serializers.ModelSerializer):
    class Meta: model = ContactMessage; fields = "__all__"

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(verified=True)
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.filter(published=True)
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ImpactStatViewSet(viewsets.ModelViewSet):
    queryset = ImpactStat.objects.filter(active=True)
    serializer_class = ImpactSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactSerializer
    http_method_names = ["get", "post", "head", "options"]
    permission_classes = [permissions.AllowAny]
