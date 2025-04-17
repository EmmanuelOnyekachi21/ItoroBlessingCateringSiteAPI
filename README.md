# Itoro Blessing Catering Backend 🍛

This is the **Django + Django REST Framework backend** of the Itoro Blessing Catering Services platform. It handles business logic, database operations, and serves APIs for the React frontend.

## 🧩 Features

- 🍱 Manage daily meal listings
- 🛒 Handle online food orders
- 🎉 Process catering service requests
- 📚 Serve cooking recipes and content
- 👩🏽‍🏫 Manage cooking lesson bookings
- 📩 Receive contact form submissions
- 🔐 Custom user model and authentication
- 🌐 RESTful API for frontend integration

## 🔧 Tech Stack

- **Framework**: Django, Django REST Framework
- **Database**: SQLite (dev), PostgreSQL (production-ready)
- **Authentication**: Token-based (or JWT via djoser/simplejwt)
- **CORS**: Enabled for frontend consumption
- **Deployment**: Render / Heroku / Railway (planned)

## 🚀 Getting Started

```bash
# Clone the backend repo
git clone git@github.com:EmmanuelOnyekachi21/ItoroBlessingCateringSiteAPI.git
cd ItoroBlessingCateringSiteAPI

# Set up a virtual environment
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```
### API available at: http://localhost:8000/api

## 📁 Project Structure
```
ItoroBlessingCateringSiteAPI/
├── catering_site/        # Django project
│   ├── settings.py
│   └── urls.py
├── catering/             # Main app (models, views, serializers)
├── manage.py
├── requirements.txt
```

## 🔗 API Endpoints (Sample)

    GET /api/meals/ – List available meals

    POST /api/orders/ – Submit an order

    POST /api/catering-request/ – Request catering

    GET /api/recipes/ – View cooking recipes

    POST /api/lessons/ – Book cooking lessons

    POST /api/contact/ – Contact Itoro Blessing

