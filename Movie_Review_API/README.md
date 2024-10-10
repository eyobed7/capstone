
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
Here’s the updated section for your README file, tailored for the **Movie Review API** with specific instructions for deployment and contributing:

---

## Deployment

To deploy the **Movie Review API** on platforms like Heroku or PythonAnywhere, follow these general steps:

1. **Create an Account**: Sign up for an account on your chosen platform (e.g., Heroku, PythonAnywhere).
2. **Create a New App**: In your dashboard, create a new application.
3. **Set Environment Variables**: Configure the required environment variables in the app settings, including:
   - `SECRET_KEY`
   - `DEBUG` (set to `False` for production)
   - Database settings
4. **Deploy Your Code**: Use Git or any other deployment method provided by the platform to push your code to the server. 
   - For Heroku: You can use the command `git push heroku main` (replace `main` with your branch name).
   - For PythonAnywhere: Follow their guide to deploy your Django application.
5. **Test Your Deployed API**: Access the public URL provided by the platform to test your API endpoints and ensure everything is functioning correctly.

## Contributing

Contributions are welcome! If you would like to contribute to the **Movie Review API**, please follow these steps:

1. **Fork the Repository**: Click on the "Fork" button at the top right of the repository page to create your copy.
2. **Create a Feature Branch**: In your local copy, create a new branch for your feature or bug fix. You can do this using the command:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make Your Changes**: Implement your changes or new features.
4. **Commit Your Changes**: Once you are satisfied with your changes, commit them:
   ```bash
   git commit -m "Add your descriptive commit message here"
   ```
5. **Push to Your Fork**: Push your changes to your forked repository:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Submit a Pull Request**: Go back to the original repository and click on the "Pull Requests" tab. Then click on "New Pull Request" and select your branch to submit your contributions for review.

---

Feel free to adjust any specific details or add additional steps that are relevant to your project. Let me know if you need further assistance!
