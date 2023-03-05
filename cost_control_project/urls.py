from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'cost_control_project'
urlpatterns = [
    path('', views.index, name='index'),
    path('check_list/', views.check_list, name='check_list'),
    path('new_check/', views.new_check, name='new_check'),
    path('edit_check/<int:check_id>/', views.edit_check, name='edit_check'),
    path('delete_check/<int:check_id>/', views.delete_check, name='delete_check'),
    path('download_upload/<int:check_id>/', views.download_upload, name='download_upload'),
    path('delete_upload/<int:check_id>/', views.delete_upload, name='delete_upload'),
    path('analyze_checks/', views.analyze_checks, name='analyze_checks'),
    path('analyze_checks_filters/', views.analyze_checks_filters, name='analyze_checks_filters'),
    path('category_list/', views.category_list, name='category_list'),
    path('new_category/', views.new_category, name='new_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)