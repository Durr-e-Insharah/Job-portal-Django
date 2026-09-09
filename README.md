# Job Portal

A full-stack job portal built with Django, connecting employers with job seekers.

## Features
- Custom user roles: Employer and Job Seeker (with interest area: Frontend/Backend/Full Stack)
- Employers can post, edit, and delete job listings (title, company, location, salary, deadline, description)
- Job seekers can browse listings and apply with a detailed application form (personal details, resume upload, cover letter with word limit)
- Employers can view all applicants for their job posts, including resume and cover letter
- Role-based permissions (only employers can post jobs, only the job owner can edit/delete)
- Django admin panel for managing users, jobs, and applications
- Custom styled UI (red-black-gold theme)

## Tech Stack
- Python, Django
- SQLite (development database)
- HTML, CSS

## Setup
1. Clone the repository
2. Create a virtual environment and activate it
3. Install dependencies: `pip install -r requirements/base.txt`
4. Create a `.env` file (see `.env.example`) with your `SECRET_KEY`
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Run the server: `python manage.py runserver`

## Project Structure
- `apps/accounts/` — custom user model, signup/login
- `apps/jobs/` — job postings, applications, CRUD views
- `templates/` — HTML templates
- `static/` — CSS