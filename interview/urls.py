# from django.urls import path
# from .views import InterviewQuestionView
# from .views import interview_page, select_role_page
# from .views import SubmitAnswerView
# from . import views
# from .views import UserAnswerListView
# from .views import dashboard_view


# urlpatterns = [
#     path('select-role/', select_role_page, name='select_role'),
#     path('', interview_page, name='interview'), 
#     path('generate/', InterviewQuestionView.as_view(), name='generate-questions'),
#     path('submit-answer/', SubmitAnswerView.as_view(), name='submit-answer'),
#     path('my-answers/', UserAnswerListView.as_view(), name='user-answers'),
#     path('dashboard/', dashboard_view, name='dashboard'),


# ]





from django.urls import path
from .views import InterviewQuestionView
from .views import interview_page, select_role_page
from .views import SubmitAnswerView
from .views import performance_analysis_view
from . import views
from .views import UserAnswerListView
from django.contrib.auth import views as auth_views
from interview.views import user_answers_view


urlpatterns = [
    path('select-role/', select_role_page, name='select_role'),
    path('', interview_page, name='interview'), 
    path('generate/', InterviewQuestionView.as_view(), name='generate-questions'),
    path('submit-answer/', SubmitAnswerView.as_view(), name='submit-answer'),
    path('performance-analysis/', performance_analysis_view, name='performance_analysis'),
    path('my-answers/', UserAnswerListView.as_view(), name='user-answers'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path("my-answers/", views.my_answers_view, name="user-answers"),
    path("api/my-answers/", UserAnswerListView.as_view(), name="api-user-answers"),
    path("my-answers/", UserAnswerListView.as_view(), name="user-answers"),
    

]