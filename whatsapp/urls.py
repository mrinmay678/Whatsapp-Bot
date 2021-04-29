from django.urls import path, include
from .views import automate, UploadCsv, tracker, downloadCSV, trackRead,upload_unknown_csv_here
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register(r'upload-csv', UploadCsv)
urlpatterns = [
    path('', automate),
    path('tracker/', tracker),
    path('trackRead/', trackRead),
    path('downloadCSV/', downloadCSV),
    path('unknown/', upload_unknown_csv_here),
]
urlpatterns += router.urls
