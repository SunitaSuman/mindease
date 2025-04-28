from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_backends
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST
from django.http import JsonResponse
from datetime import date, timedelta
from django.utils.timezone import now

import os

import json
from .models import MOOD_CHOICES
from django.db.models import Count

from .forms import MoodEntryForm, CustomUserCreationForm
from .models import MoodEntry, JournalEntry, DailyTask, UserProfile, TodoItem, WellnessLog
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
# @login_required
# def profile(request):
#     user = request.user
#     mood_count = MoodEntry.objects.filter(user=user).count()
#     journal_count = JournalEntry.objects.filter(user=user).count()
#     task_days = DailyTask.objects.filter(user=user).count()
    
#     if request.method == 'POST':
#         form = PasswordChangeForm(user, request.POST)
#         if form.is_valid():
#             form.save()
#             update_session_auth_hash(request, form.user)  # Important!
#             messages.success(request, 'Password updated successfully.')
#             return redirect('profile')
#     else:
#         form = PasswordChangeForm(user)

#     return render(request, 'accounts/profile.html', {
#         'user': user,
#         'mood_count': mood_count,
#         'journal_count': journal_count,
#         'task_days': task_days,
#         'form': form
#     })



# -------------------- Auth Views --------------------

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}! 🌟")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Set backend manually
            backend = get_backends()[0]
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"

            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


# -------------------- Public View --------------------

def home(request):
    return render(request, 'accounts/home.html')


# -------------------- Dashboard --------------------

@login_required
def dashboard(request):
    latest_mood = MoodEntry.objects.filter(user=request.user).order_by('-timestamp').first()
    latest_journal = JournalEntry.objects.filter(user=request.user).order_by('-created_at').first()
    tasks_today = DailyTask.objects.filter(user=request.user, date=date.today())
    todo_items = TodoItem.objects.filter(user=request.user).order_by('completed', '-created_at')[:5]  # Limit for brevity

    return render(request, 'accounts/dashboard.html', {
        'latest_mood': latest_mood,
        'latest_journal': latest_journal,
        'tasks_today': tasks_today,
        'todo_items': todo_items,
    })


# -------------------- Mood Tracker --------------------

@login_required
def mood_tracker(request):
    if request.method == 'POST':
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            mood = form.save(commit=False)
            mood.user = request.user
            mood.save()
            return redirect('mood_tracker')
    else:
        form = MoodEntryForm()

    moods = MoodEntry.objects.filter(user=request.user).order_by('-timestamp')[:7]
    return render(request, 'accounts/mood_tracker.html', {'form': form, 'moods': moods})


# -------------------- Journal Views --------------------

@login_required
@require_http_methods(["GET", "POST"])
def journal(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        title = request.POST.get("title")
        entry = request.POST.get("entry")
        tags = request.POST.get("tags")

        new_entry = JournalEntry.objects.create(
            user=request.user,
            title=title,
            entry=entry,
            tags=tags
        )

        return JsonResponse({
            "id": new_entry.id,
            "title": new_entry.title,
            "entry": new_entry.entry[:200],  # truncated
            "tags": new_entry.tags,
            "created_at": new_entry.created_at.strftime("%b %d, %Y"),
            "is_today": new_entry.created_at.date() == now().date()
        })

    # Regular GET request:
    all_entries = JournalEntry.objects.filter(user=request.user).order_by("-created_at")
    today = now().date()
    return render(request, "accounts/journal.html", {
        "all_entries": all_entries,
        "today": today
    })


@login_required
@require_http_methods(["GET", "POST"])
def edit_journal_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, pk=entry_id, user=request.user)

    if request.method == "POST":
        entry.title = request.POST.get("title", "").strip() or f"Journal Entry - {entry.created_at.strftime('%Y-%m-%d')}"
        entry.entry = request.POST.get("entry", "").strip()
        entry.tags = request.POST.get("tags", "").strip()
        entry.save()
        return redirect("journal")

    all_entries = JournalEntry.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "accounts/journal.html", {
        "entry": entry,
        "editing": True,
        "all_entries": all_entries,
        "today": date.today(),
    })


# -------------------- Daily Tasks --------------------

@login_required
def daily_tasks(request):
    today = date.today()
    daily_task, created = DailyTask.objects.get_or_create(user=request.user, date=today)

    tasks = ['water_intake', 'breakfast', 'lunch', 'dinner', 'shower', 'workout', 'sleep', 'meditation']
    task_status = {task: getattr(daily_task, task, False) for task in tasks}

    completed = sum(1 for task in tasks if getattr(daily_task, task))
    total = len(tasks)
    percentage = int((completed / total) * 100) if total > 0 else 0

    return render(request, 'accounts/daily_task.html', {
        'daily_task': daily_task,
        'tasks': tasks,
        'task_status': task_status,
        'completed': completed,
        'total': total,
        'percentage': percentage
    })


@login_required
@require_POST
def update_task_status(request):
    try:
        data = json.loads(request.body)
        task_name = data.get('task_name')
        status = data.get('status')

        if not task_name:
            return JsonResponse({'success': False, 'error': 'Task name is required'})

        # Convert string 'true'/'false' to boolean
        if isinstance(status, str):
            status = status.lower() == 'true'

        task, _ = DailyTask.objects.get_or_create(user=request.user, date=date.today())

        if hasattr(task, task_name):
            setattr(task, task_name, status)
            task.save()
        else:
            return JsonResponse({'success': False, 'error': f'Invalid task name: {task_name}'})

        total_tasks = 8
        completed_tasks = sum(1 for field in ['water_intake', 'breakfast', 'lunch', 'dinner', 'shower', 'workout', 'sleep', 'meditation'] if getattr(task, field) == True)
        percentage = (completed_tasks / total_tasks) * 100

        return JsonResponse({'success': True, 'percentage': percentage})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# -------------------- Utility View --------------------

def some_view(request):
    show_logout_button = request.user.is_authenticated and request.path not in ['/login/', '/signup/', '/']
    return render(request, 'your_template.html', {'show_logout_button': show_logout_button})


from django.shortcuts import get_object_or_404, redirect
from .models import JournalEntry


@login_required
def delete_journal_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
    entry.delete()
    return redirect('journal')  # change to your journal page's name if different



# -------------------- Profile View --------------------
from random import choice
def get_daily_suggestion():
    # List of daily motivational suggestions
    suggestions = [
        "Keep going, you're stronger than you think!",

"Believe in yourself, you’ve got this!",

"Every day is a new opportunity to grow.",

"Don’t stop now, you’re almost there!",

"Your hard work will lead to amazing results!",

"Stay focused, your dreams are within reach!",

"You’re making progress, even if it feels slow.",

"Great things take time, keep pushing forward!",

"Success is the sum of small efforts repeated daily.",

"The only limit is the one you set for yourself!",
    ]
    return choice(suggestions)

from django.utils.timezone import now
from datetime import date, timedelta
from django.db.models.functions import TruncDate




@login_required
def profile(request):
    user = request.user

    profile, created = UserProfile.objects.get_or_create(user=user)

    today = date.today()
    mood_count = MoodEntry.objects.filter(user=user).count()
    journal_count = JournalEntry.objects.filter(user=user).count()
    last_week = today - timedelta(days=6)
    recent_moods = MoodEntry.objects.filter(user=user, timestamp__date__gte=last_week).order_by('-timestamp')

    mood_data = {mood[0]: MoodEntry.objects.filter(user=user, mood=mood[0]).count() for mood in MOOD_CHOICES}


    mood = recent_moods[0].mood if recent_moods else None
    recommendation = ""

    if mood == "sad":
        recommendation = "You’re feeling low today. Try a warm cup of tea, light stretching, or a short chat with a friend."
    elif mood == "tired" and 'Exercise' in [task.name for task in uncompleted_tasks]:
        recommendation = "Feeling tired? A short walk or light yoga might energize you."
    elif mood == "happy" :
        recommendation = "You’re happy! Keep the momentum by ticking off more tasks. 💪"
    elif mood == "anxious":
        recommendation = "Feeling anxious? Try some deep breathing or a short meditation session."
    elif mood == "angry":
        recommendation = "Feeling angry? A quick workout or a walk can help release that energy."
    elif mood == "meh":
        recommendation = "Feeling neutral? It’s a good day to focus on self-care tasks and reflect."

    todays_tasks = DailyTask.objects.filter(user=user, date=today)
    task_days = todays_tasks.count()

    task_fields = [
        'water_intake', 'breakfast', 'lunch', 'dinner', 
        'shower', 'workout', 'sleep', 'meditation'
    ]

    motivations = {
        "Water Intake": "Stay hydrated, your brain needs it!",
        "Workout": "Move your body, boost your mood!",
        "Sleep": "Rest well to feel your best!",
        "Meditation": "A calm mind brings inner strength.",
        "Breakfast": "Kickstart your day with a healthy breakfast!",
        "Lunch": "Refuel your energy mid-day!",
        "Dinner": "Wind down your day with something nutritious.",
        "Shower": "Feel fresh and reset with a quick shower!",
    }

    total_possible = task_days * len(task_fields)
    task_completion = 0
    completed_tasks = []
    uncompleted_tasks = []
    uncompleted_task_motivations = []

    for task in todays_tasks:
        checked = task.get_checked_tasks()
        completed_tasks.extend([task_name.capitalize() for task_name in checked])
        task_completion += len(checked)
        
        for task_name in task_fields:
            if not getattr(task, task_name):
                readable = task_name.replace("_", " ").capitalize()
                uncompleted_tasks.append(readable)
                uncompleted_task_motivations.append({
                    "name": readable,
                    "motivation": motivations.get(readable, "You're doing great – keep it up!")
                })

    completion_percentage = (task_completion / total_possible * 100) if total_possible > 0 else 0
    total_tasks = len(task_fields)
    completed_tasks_count = len(completed_tasks)
    completion_percent = (completed_tasks_count / total_tasks) * 100 if total_tasks > 0 else 0

    if not uncompleted_tasks:
        uncompleted_tasks_message = "You've completed all your self-care tasks today!"
    else:
        uncompleted_tasks_message = f"Uncompleted tasks: {', '.join(uncompleted_tasks)}"

    
    last_7_days = timezone.now().date() - timedelta(days=6)
    weekly_data = MoodEntry.objects.filter(user=user, timestamp__date__gte=last_7_days)
    weekly_counts = (
        weekly_data
        .annotate(day=TruncDate('timestamp'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    weekly_mood_data = {
        entry['day'].strftime('%b %d'): entry['count']
        for entry in weekly_counts
    }

    password_form = PasswordChangeForm(user)
    latest_journal_entry = JournalEntry.objects.filter(user=user).order_by('-created_at').first()
    daily_motivation = get_daily_suggestion()

    return render(request, 'accounts/profile.html', {
        'user': user,
        'profile': profile,
        'mood_count': mood_count,
        'journal_count': journal_count,
        'task_days': task_days,
        'completion_percentage': round(completion_percentage),
        'task_completion': task_completion,
        'total_possible': total_possible,
        'completed_tasks': completed_tasks,
        'uncompleted_tasks': uncompleted_tasks,
        'uncompleted_task_motivations': uncompleted_task_motivations,
        'uncompleted_tasks_message': uncompleted_tasks_message,
        'recent_moods': recent_moods,
        'mood_data': mood_data,
        'password_form': password_form,
        'mood_choices': MOOD_CHOICES,
        'completion_percent': round(completion_percent),
        'latest_journal_entry': latest_journal_entry,
        'weekly_mood_data': weekly_mood_data,
        'daily_motivation': daily_motivation,
        "recommendation": recommendation,
    })



@login_required
@require_http_methods(["POST"])
def update_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    # Handle profile picture upload
    if 'profile_picture' in request.FILES:
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        messages.success(request, "Profile picture updated successfully!")

    # Handle password change
    if 'old_password' in request.POST:
        password_form = PasswordChangeForm(user, request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)  # Keep the user logged in
            messages.success(request, "Password updated successfully!")
        else:
            for error in password_form.errors.values():
                messages.error(request, error)

    return redirect('profile')




# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import TodoItem
from django.contrib.auth.decorators import login_required

@login_required
def todo_list(request):
    todos = TodoItem.objects.filter(user=request.user)
    return render(request, 'accounts/todo_list.html', {'todos': todos})

@login_required
def add_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            TodoItem.objects.create(user=request.user, title=title)
    return redirect('todo_list')

@login_required
def toggle_todo(request, todo_id):
    todo = get_object_or_404(TodoItem, id=todo_id, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')

@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(TodoItem, id=todo_id, user=request.user)
    todo.delete()
    return redirect('todo_list')


from django.utils import timezone

def get_weekly_mood_data(user):
    today = timezone.now()
    one_week_ago = today - timedelta(days=7)
    moods = MoodEntry.objects.filter(user=user, timestamp__gte=one_week_ago)
    
    # Calculate the average mood for each day in the last week
    mood_counts = {
        "Happy": 0,
        "Sad": 0,
        "Neutral": 0,
    }
    
    for mood in moods:
        mood_counts[mood.get_mood_display()] += 1
    
    return mood_counts


import os
import openai
openai.api_key = os.getenv('OPENAI_API_KEY')

@login_required
def ai_chatbot(request):
    ai_response = ""
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ]
            )
            ai_response = response.choices[0].message.content
        except Exception as e:
            ai_response = f"Error: {str(e)}"
    return render(request, 'accounts/ai_chatbot.html', {'ai_response': ai_response})



@login_required
def wellness_tracking(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_log = WellnessLog.objects.create(
                user=request.user,
                sleep_duration=float(data.get('sleep_duration', 0)),
                screen_time=float(data.get('screen_time', 0)),
                outdoor_time=float(data.get('outdoor_time', 0)),
                exercise_time=float(data.get('exercise_time', 0))
            )
            
            # Get updated logs
            today = timezone.now().date()
            last_7_days = today - timedelta(days=6)
            logs = WellnessLog.objects.filter(
                user=request.user,
                date__range=[last_7_days, today]
            ).order_by('date')
            
            # Serialize logs for JSON response
            logs_data = [{
                'date': log.date.strftime('%Y-%m-%d'),
                'sleep_duration': log.sleep_duration,
                'screen_time': log.screen_time,
                'outdoor_time': log.outdoor_time,
                'exercise_time': log.exercise_time
            } for log in logs]
            
            recommendations = new_log.get_recommendation()
            compliment = all([
                7 <= new_log.sleep_duration <= 9,
                new_log.screen_time <= 6,
                new_log.outdoor_time >= 1,
                new_log.exercise_time >= 30
            ])
            
            return JsonResponse({
                'status': 'success',
                'logs': logs_data,
                'recommendations': recommendations,
                'compliment': compliment
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    # GET request
    today = timezone.now().date()
    last_7_days = today - timedelta(days=6)
    logs = WellnessLog.objects.filter(
        user=request.user,
        date__range=[last_7_days, today]
    ).order_by('date')

    # Serialize logs for template
    logs_data = [{
        'date': log.date.strftime('%Y-%m-%d'),
        'sleep_duration': log.sleep_duration,
        'screen_time': log.screen_time,
        'outdoor_time': log.outdoor_time,
        'exercise_time': log.exercise_time
    } for log in logs]

    latest_log = logs.last()
    if latest_log:
        recommendations = latest_log.get_recommendation()
        compliment = all([
            7 <= latest_log.sleep_duration <= 9,
            latest_log.screen_time <= 6,
            latest_log.outdoor_time >= 1,
            latest_log.exercise_time >= 30
        ])
    else:
        recommendations = []
        compliment = False

    context = {
        'logs': logs_data,
        'recommendations': recommendations,
        'compliment': compliment
    }

    return render(request, 'accounts/wellness_tracking.html', context)


def resource(request):
    return render(request, 'accounts/resource.html')