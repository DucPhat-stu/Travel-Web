from rest_framework.routers import DefaultRouter
from .api import DestinationViewSet, PackageViewSet, ReviewViewSet, CommentViewSet

router = DefaultRouter()
router.register(r"destinations", DestinationViewSet, basename="destination")
router.register(r"packages", PackageViewSet, basename="package")
router.register(r"reviews", ReviewViewSet, basename="review")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = router.urls

