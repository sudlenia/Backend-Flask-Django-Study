
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import SignUpView
from blogs.views import PostsViewSet, CommentsViewSet, PostCreateViewSet

router = DefaultRouter()
router.register(r'posts', PostsViewSet, basename='posts')

posts_router = NestedDefaultRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentsViewSet, basename='post-comments')

urlpatterns = [

    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
    path('posts/', include('blogs.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('api/', include(router.urls)),
    path('api/', include(posts_router.urls)),
    path('api/create/post', PostCreateViewSet.as_view(), name='post_create'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
