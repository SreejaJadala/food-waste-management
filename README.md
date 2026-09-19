# Smart Food Waste Management & Analytics System

A beginner-friendly Django application for food providers, NGOs, and administrators. MySQL stores the main users, food-waste, donations, and collection records. MongoDB stores a secondary history/activity trail.

## What is already included

- Role-based registration and session login: Admin, Food Provider, NGO/Volunteer
- REST API CRUD for food-waste records at `/api/food/waste/`
- Donation creation and collection lifecycle at `/api/donations/`
- Pandas/NumPy summary API at `/api/analytics/summary/`
- Matplotlib chart generator at `/api/analytics/charts/`
- HTML/CSS/JavaScript dashboard using `fetch()`
- MongoDB history logging that does not stop the main system if MongoDB is unavailable

## Setup, step by step

1. Install MySQL and MongoDB, and start both services.
2. In MySQL, create the database:

```sql
CREATE DATABASE food_waste_db CHARACTER SET utf8mb4;
```

3. In this project folder, copy `.env.example` to `.env` and set `MYSQL_PASSWORD` (and any different MySQL/MongoDB connection values). Never commit `.env`.
4. Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

5. Install packages:

```powershell
pip install -r requirements.txt
```

6. Create database migration files, then apply them. This is the first required database test:

```powershell
python manage.py makemigrations users food donation
python manage.py migrate
python manage.py check
```

7. Create an administrator account and start the server:

```powershell
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/register/` to create a provider or NGO account. Use `http://127.0.0.1:8000/admin/` for Django administration.

## Module-by-module quick test

1. **Users:** Register, then log in. The dashboard should display your name and role.
2. **Food:** Open **Food waste**, add a record, and confirm it appears in the table and in `GET /api/food/waste/`.
3. **Analytics:** Open **Analytics**, verify the metrics, then select **Generate Matplotlib charts**. PNG files are created in `static/charts/`.
4. **Donation:** Use a logged-in provider to `POST /api/donations/`; an NGO user can call `POST /api/donations/<id>/claim/` and then `/collect/`.
5. **MongoDB:** When MongoDB is running, inspect database `food_waste_history` and its `waste_history`, `activity_history`, and `collection_history` collections.

## API examples

Use Django's browsable API in a browser while logged in, or a REST client with the session/CSRF token.

- `GET`, `POST /api/food/waste/`
- `GET`, `PUT`, `PATCH`, `DELETE /api/food/waste/<id>/`
- `GET`, `POST /api/donations/`
- `POST /api/donations/<id>/claim/`
- `POST /api/donations/<id>/collect/`
- `GET /api/analytics/summary/`
- `POST /api/analytics/charts/`

- http://127.0.0.1:8000/register/

- Separate role-based dashboards:
  - Admin: `/dashboard/admin/`
  - Food Provider: `/dashboard/provider/`
  - NGO/Volunteer: `/dashboard/ngo/`
- The root URL `/` redirects each logged-in user to the correct dashboard automatically.
A valid food waste JSON body is:

```json
{"source":"Main Canteen","food_type":"Rice","prepared_quantity":30,"wasted_quantity":4.5,"date":"2026-09-17"}
```

## Future extension points

Keep prediction code in `analytics/`, create matching logic in `donation/`, add notification services as a separate app, and use the summary data for monthly/exported reports.
