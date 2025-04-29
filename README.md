# MindEase – Mental Health Web Application

**Deployed Link**: [MindEase - Live Demo](https://mindease-nx4j.onrender.com)

## Project Overview

MindEase is an AI-integrated mental wellness web application designed to help users track their mental health through daily self-care tasks, mood tracking, journaling, and personalized wellness recommendations. It combines features of task management, mood entries, journaling, and motivational support to provide a comprehensive solution for improving mental health and well-being.

## Features

- **User Authentication**: Secure login/signup system with custom user authentication. Profile management and password change functionality included.
- **Daily Tasks**: Track daily self-care tasks like water intake, meals, exercise, and sleep. Visual task progress bar shows completion percentage.
- **Mood Tracker**: Users can log daily moods with descriptive notes and view a history of mood logs.
- **Journaling**: Create and edit journal entries with titles, tags, and detailed content. AI-powered dynamic prompts for better reflection.
- **AI-Driven Wellness Suggestions**: Personalized suggestions based on mood and task completion (e.g., meditate, go for a walk).
- **Profile Page**: Displays user statistics such as total mood entries, journals, and completed tasks.
- **Responsive UI**: Built using Bootstrap and TailwindCSS. Fully responsive design for mobile, tablet, and desktop. Dark mode support included.
- **Real-Time Updates**: AJAX integration for seamless updates on journal entries and daily task progress without page reloads.
- **Motivational Messages**: Dynamic daily affirmations and motivation tips to boost positivity and mental wellness.

## Tech Stack

- **Backend**: Django 5.2
- **Frontend**: HTML5, CSS3 (Bootstrap, TailwindCSS)
- **Database**: SQLite3 (Development) / PostgreSQL (Production)
- **User Authentication**: Django custom user model
- **AI Integration**: Randomized wellness suggestion logic
- **Deployment**: Local or Cloud platforms like AWS, Heroku, Render

## Project Structure

mindbloom/ ├── mindbloom/ # Django project settings ├── accounts/ # User authentication app ├── tracker/ # Mood tracking, journaling, tasks app ├── templates/ # HTML templates ├── static/ # Static files (CSS, JS, Images) ├── media/ # Uploaded files (profile images, etc.) ├── manage.py # Django management script └── requirements.txt # Project dependencies

markdown
Copy
Edit

## Installation

### Prerequisites

- Python 3.8+
- Django 5.2
- pip (Python package installer)

### Setup Steps

1. Clone the repository:

```bash
git clone https://github.com/username/mindbloom.git
cd mindbloom
Create and activate a virtual environment:


python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
Install dependencies:


pip install -r requirements.txt
Set up the database:


python manage.py migrate
Create a superuser for admin access:


python manage.py createsuperuser
Run the development server:


python manage.py runserver
Visit the application:

Open your browser and go to: http://127.0.0.1:8000/

```

Future Scope
Launch a mobile app for Android and iOS.

Integration with external APIs like Google Books or Goodreads.

Implement voice-based journaling and mood tracking.

Blockchain-based secure data handling.

Add multi-language support for global users.

Contributing
Contributions are welcome! Feel free to fork the repository, create a feature branch, make your changes, and submit a pull request.

License
This project is open-source and available under the MIT License.

Contact
For queries, feedback, or collaboration opportunities:

Name: Sunita Kumari

Email: summu.sunita345@gmail.com

LinkedIn: Sunita Kumari










