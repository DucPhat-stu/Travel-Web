from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from users.api import UserViewSet, ObtainAPITokenView
from tours.api import TourViewSet
from hotels.api import HotelViewSet
from flight.api import FlightViewSet
from bookings.api import BookingViewSet
from chatbot.api import ChatMessageViewSet
from catalog.api import (
    DestinationViewSet,
    PackageViewSet,
    ReviewViewSet,
    CommentViewSet,
    PlannerSearchView,
    TripQuoteView,
)

app_name = "api"

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"tours", TourViewSet, basename="tour")
router.register(r"hotels", HotelViewSet, basename="hotel")
router.register(r"flights", FlightViewSet, basename="flight")
router.register(r"bookings", BookingViewSet, basename="booking")
router.register(r"chat-messages", ChatMessageViewSet, basename="chatmessage")
router.register(r"destinations", DestinationViewSet, basename="destination")
router.register(r"packages", PackageViewSet, basename="package")
router.register(r"reviews", ReviewViewSet, basename="review")
router.register(r"comments", CommentViewSet, basename="comment")

schema_view = get_schema_view(
    openapi.Info(
        title="Travel API",
        default_version="v1",
        description="Tài liệu REST API cho dự án Travel-Web",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/token/", ObtainAPITokenView.as_view(), name="api-token"),
    path("planner/search/", PlannerSearchView.as_view(), name="planner-search"),
    path("planner/quote-trip/", TripQuoteView.as_view(), name="planner-quote-trip"),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "docs/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

