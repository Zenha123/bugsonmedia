from django.urls import path # type: ignore
from . import views

urlpatterns = [
    #path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('weekly-quiz/', views.weekly_quiz, name='weekly_quiz'),
    path('quiz-complete/', views.quiz_complete, name='quiz_complete'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('history/', views.quiz_history, name='quiz_history'),
]