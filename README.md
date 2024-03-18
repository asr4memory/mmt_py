Python version of MMT software

*This software is experimental.*

## Requirements

- Python 3.12 (tested with 3.12, likely runs with older versions)
- ffmpeg

## Installation

- Create virtual environment
- Install requirements with `pip install -r requirements.txt`
- Install Node.js requirements with `npm install`
- run `python manage.py migrate` to run the database migrations
- Optional: Create admin user with `python manage.py createsuperuser`

## Usage

- Run `python manage.py runserver`
- Run the webpack dev server with `npm run devserver` (in another terminal)
- Visit 127.0.0.1:8000/ in your browser
- The admin interface is located at 127.0.0.1:8000/admin/
