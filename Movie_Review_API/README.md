
# Movie Review API

## Project Overview
The **Movie Review API** is a backend solution built using Django and Django REST Framework (DRF). This API allows users to submit, view, and manage movie reviews, including rating movies and posting comments. It serves as a foundation for any application that requires user-generated content on movie reviews and ratings.

## Table of Contents
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Contributing](#contributing)

## Installation
To set up the Movie Review API locally, follow these steps:

### Clone the repository:

```bash
git clone https://github.com/yourusername/movie_review_api.git
cd movie_review_api
```

### Create a virtual environment:

```bash
python -m venv .venv
```

### Activate the virtual environment:

- On Windows:
  ```bash
  .venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source .venv/bin/activate
  ```

### Install the required packages:

```bash
pip install -r requirements.txt
```

### Apply migrations:

```bash
python manage.py migrate
```

### Create a superuser (for admin access):

```bash
python manage.py createsuperuser
```

## Configuration

- **Environment Variables**: Set up the required environment variables, such as `SECRET_KEY`, `DEBUG`, and database settings.
- **Settings**: Update the `settings.py` file to configure installed apps, middleware, and authentication backends as necessary.

## Usage

### Run the development server:

```bash
python manage.py runserver
```

### Access the API:
Here’s how you can update your README file to include the full URLs for each of the API endpoints, prefixed with `http://127.0.0.1:8000/`. This will make it clear to users how to access each endpoint:

---

## API Endpoints

Here are the available API endpoints for the **Movie Review API**:

### Reviews

- **List all reviews**  
  `GET` `http://127.0.0.1:8000/reviews/`
  
- **Create a review**  
  `POST` `http://127.0.0.1:8000/reviews/create/`
  
- **Retrieve a single review by ID**  
  `GET` `http://127.0.0.1:8000/reviews/<int:pk>/`
  
- **Update a review by ID**  
  `PUT` `http://127.0.0.1:8000/reviews/<int:pk>/update/`
  
- **Delete a review by ID**  
  `DELETE` `http://127.0.0.1:8000/reviews/<int:pk>/delete/`

### User Authentication

- **Register a new user**  
  `POST` `http://127.0.0.1:8000/register/`
  
- **User login**  
  `POST` `http://127.0.0.1:8000/login/`
  
- **User logout**  
  `POST` `http://127.0.0.1:8000/logout/`

### Likes

- **Like a review**  
  `POST` `http://127.0.0.1:8000/reviews/<int:pk>/like/`
  
- **Unlike a review**  
  `POST` `http://127.0.0.1:8000/reviews/<int:pk>/unlike/`
  
- **See the most liked reviews for a specific movie**  
  `GET` `http://127.0.0.1:8000/reviews/likes/<str:movie_title>/`

### Profile

- **View user profile**  
  `GET` `http://127.0.0.1:8000/profile/<str:username>/`
  
- **Create or update a user profile**  
  `POST` `http://127.0.0.1:8000/profileform/`

### Comments

- **List comments related to a specific review**  
  `GET` `http://127.0.0.1:8000/reviews/<int:pk>/comments/`
  
- **Create a new comment for a specific review**  
  `POST` `http://127.0.0.1:8000/reviews/<int:pk>/comments/create/`

### Most Reviewed Movies

- **View for most reviewed movies**  
  `GET` `http://127.0.0.1:8000/`

---

### Notes:
- Replace `<int:pk>` with the actual review ID and `<str:movie_title>` with the actual movie title when making requests.
- For the `register`, `login`, and `profileform` endpoints, ensure to use the appropriate HTTP methods as indicated.

This structure will help users easily understand how to interact with your API. Let me know if you need further modifications!

Feel free to add any project-specific details or API endpoint documentation!
