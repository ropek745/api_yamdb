from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet,
                    TitleViewSet, UserViewSet, get_token, signup
)

app_name = 'api'

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

auth_patterns = [
    path('token/', get_token),
    path('signup/', signup)
]


urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router.urls), name='api')
]
