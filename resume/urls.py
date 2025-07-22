from django.urls import path
from .views import ResumeUploadView
from .views import resume_upload_html
from .views import ResumeParsedDataView

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='resume-upload'),
    path('upload/html/', resume_upload_html, name='resume-upload-html'),
    path('parsed/', ResumeParsedDataView.as_view(), name='resume-parsed'),
]
