from django.urls import path, include
from django.contrib import admin

from gmuesabo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('impersonate/', include('impersonate.urls')),
    path('', include('juntagrico.urls')),
    path('',include('juntagrico_billing.urls')),
    path('manage/subscription/shares', views.SubscriptionSharesView.as_view(), name='manage-subscription-shares'),
]
