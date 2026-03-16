# F25 Discovery Project

This repository contains a Django application developed for the F25 Discovery course.

## Project Structure

accounts/ – Django app handling account management  
models.py – Database models  
views.py – Application views  
urls.py – URL routing  
forms.py – Form definitions  

## Setup

1. Create virtual environment
2. Install dependencies

pip install -r requirements.txt

3. Run migrations

python manage.py migrate

4. Start server

python manage.py runserver