Heroes of Git and Hub
===

Heroes of Git and hub is game where you becomes a hero and your repositories in Github transforms to your army. Demo version is available at http://hgh.dev8.ru


Installation
===
1. Clone repo
2. Run `pip install -r requirements.txt`
3. Create application in Github account settings and set GITHUB_APP_ID and GITHUB_API_SECRET in `hgh/settings.py`
4. Run `python manage.py syncdb`
5. Run `python manage.py migrate`
6. Run `python manage.py runserver`
7. Open in your browser http://localhost:8000/
8. Add to cronjobs (hourly) `python path/to/project/crons/update_heroes.py` to auto update heroes and army