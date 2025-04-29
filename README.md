# MindEase – Mental Health Web Application

**Deployed Link**: [MindEase - Live Demo](https://mindease-nx4j.onrender.com)

## Project Overview

**MindEase** is an AI-integrated mental wellness web application designed to help users track their mental health through daily self-care tasks, mood tracking, journaling, and personalized wellness recommendations. It combines features of task management, mood entries, journaling, and motivational support to provide a comprehensive solution for improving mental health and well-being.

## Features

### 🛠️ **User Authentication**
- Custom authentication system with secure login/signup.
- Profile management and password change functionalities.

### 📅 **Daily Tasks**
- Users can track their daily self-care tasks (e.g., water intake, breakfast, sleep, meditation).
- Task progress is visualized with a percentage tracker, showing completion status.

### 💭 **Mood Tracker**
- Users can log their mood entries along with descriptive notes.
- Displays a history of mood logs, with an option to add new entries.

### 📝 **Journaling**
- Users can create and edit journal entries, with options to add titles, tags, and detailed descriptions.
- Supports dynamic journaling with AI-powered prompts for better self-reflection.

### 🤖 **AI-Driven Wellness Suggestions**
- Based on mood entries and task completion, the app provides personalized wellness suggestions for the day (e.g., take a break, go for a walk, meditate).

### 👤 **Profile Page**
- Displays user statistics such as total mood entries, journal entries, and daily tasks completed.
- Users can view and edit their profile information.

### 📱 **Responsive UI**
- The app is built with a mobile-responsive interface using Bootstrap and TailwindCSS.
- Dark mode support for a comfortable viewing experience at night.

### 🔄 **Real-Time Updates**
- AJAX-based updates for journal entries and daily tasks to ensure a seamless user experience without page reloads.

### ✨ **Motivational Messages**
- Dynamic daily affirmations and suggestions are provided to encourage users to stay on track with their mental wellness journey.

## Technologies

- **Backend**: Django 5.2
- **Frontend**: HTML, CSS (Bootstrap & TailwindCSS)
- **Database**: SQLite (or PostgreSQL for production)
- **User Authentication**: Custom user model with Django's authentication system
- **AI Integration**: Randomized daily wellness suggestions based on user input
- **Deployment**: Local development server or production-ready deployment (to be configured on cloud platforms such as AWS or Heroku)

## Installation

### Prerequisites

- Python 3.8+
- Django 5.2
- pip (Python package installer)

### Installation Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/username/mindbloom.git
   cd mindbloom
