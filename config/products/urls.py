from django.urls import path
from products import views

urlpatterns = [
    path("advertisements/", views.AdvertisementView.as_view(), name="advertisements"),
    path(
        "alladvertisements/",
        views.AllAdvertisementsView.as_view(),
        name="alladvertisements",
    ),
    path(
        "advertisementdetail/",
        views.AdvertisementDetailView.as_view(),
        name="advertisementdetail",
    ),
]
