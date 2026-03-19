from django.contrib import admin
from django.urls import path
from dashboard.views import (
    home, profile_list_view, search_suggest,
    score_result_view, score_detail_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('profiles/', profile_list_view, name='profiles'),
    path('profiles/suggest/', search_suggest, name='search_suggest'),
    path('profiles/<int:pk>/result/', score_result_view, name='score_result'),
    path('profiles/<int:pk>/detail/', score_detail_view, name='score_detail'),
]