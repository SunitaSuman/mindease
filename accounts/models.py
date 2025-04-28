from django.db import models
from django.contrib.auth.models import User
from datetime import date

MOOD_CHOICES = [
    ('happy', '😊 Happy'),
    ('sad', '😢 Sad'),
    ('anxious', '😰 Anxious'),
    ('angry', '😡 Angry'),
    ('tired', '😴 Tired'),
    ('meh', '😐 Meh'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"


class MoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    note = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mood} @ {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True, default="Journal Entry")  # Make title optional with default
    entry = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Journal by {self.user.username} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    

from django.db import models
from django.contrib.auth.models import User
from datetime import date as dt_date  # Avoid conflict with field name 'date'

class DailyTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=dt_date.today)  # Automatically set today's date

    # Boolean fields for daily tasks
    water_intake = models.BooleanField(default=False)
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)
    shower = models.BooleanField(default=False)
    workout = models.BooleanField(default=False)
    sleep = models.BooleanField(default=False)
    meditation = models.BooleanField(default=False)

    # Method to return only completed tasks
    def get_checked_tasks(self):
        checked_tasks = []
        task_fields = ['water_intake', 'breakfast', 'lunch', 'dinner', 'shower', 'workout', 'sleep', 'meditation']
        for task in task_fields:
            if getattr(self, task):
                checked_tasks.append(task)
        return checked_tasks

    def __str__(self):
        return f"Daily tasks for {self.user.username} on {self.date}"

    class Meta:
        unique_together = ('user', 'date')  # Only one entry per user per day



class TodoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title





from django.db import models
from django.contrib.auth.models import User

class WellnessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sleep_duration = models.FloatField(help_text="Hours slept")
    screen_time = models.FloatField(help_text="Hours of screen time")
    outdoor_time = models.FloatField(help_text="Hours spent outdoors")
    exercise_time = models.FloatField(help_text="Minutes of exercise")
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def get_recommendation(self):
        recommendations = []
        if self.sleep_duration < 7:
            recommendations.append("Try to get more sleep! Aim for 7-9 hours for better mental health.")
        elif self.sleep_duration > 9:
            recommendations.append("You're getting plenty of sleep! Make sure it's quality rest.")

        if self.screen_time > 2:
            recommendations.append("Consider reducing screen time and taking regular breaks.")

        if self.outdoor_time < 1:
            recommendations.append("Try to spend more time outdoors for vitamin D and fresh air!")

        if self.exercise_time < 30:
            recommendations.append("Aim for at least 30 minutes of exercise daily for better health.")
        elif self.exercise_time >= 60:
            recommendations.append("Great job staying active! Keep up the good work! 💪")

        return recommendations or ["You're doing well! Keep maintaining this healthy balance."]