from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),  # Root path
    path("dashboard/", views.dashboard, name="dashboard"),
    path('mood_tracker/', views.mood_tracker, name='mood_tracker'),
    path('daily_tasks/', views.daily_tasks, name='daily_tasks'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    path('journal/', views.journal, name='journal'),
    path('journal/edit/<int:entry_id>/', views.edit_journal_entry, name='edit_journal_entry'),
     path('journal/delete/<int:entry_id>/', views.delete_journal_entry, name='delete_journal_entry'),

    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('update-task-status/', views.update_task_status, name='update_task_status'),
    path('ai_chatbot/', views.ai_chatbot, name='ai_chatbot'),
     path('todo/add/', views.add_todo, name='add_todo'),
    path('todo/<int:todo_id>/toggle/', views.toggle_todo, name='toggle_todo'),
    path('todo/<int:todo_id>/delete/', views.delete_todo, name='delete_todo'),
    path('todo/', views.todo_list, name='todo_list'),
    path('wellness/', views.wellness_tracking, name='wellness_tracking'),
    path('resource/', views.resource, name='resource'),
    ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 