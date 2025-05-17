# Travelling - Travel Booking Website

A modern travel booking website built with Django that allows users to search and book various travel services including hotels, flights, car rentals, and cruises.

## Features

- Search functionality for multiple travel categories
- Destination autocomplete
- Date-based booking system
- User authentication
- Responsive design
- Beautiful modern UI

## Tech Stack

- Django 5.2
- Python 3.x
- Bootstrap 4
- jQuery
- HTML5/CSS3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Mcdtronix/Travelling.git
cd Travelling
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Load initial data:
```bash
python manage.py setup_initial_data
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see the website.

## Project Structure

- `core/` - Main application directory
  - `models.py` - Database models
  - `views.py` - View logic
  - `urls.py` - URL routing
  - `admin.py` - Admin interface configuration
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS, images)
- `Travel/` - Project configuration directory

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Template design by Colorlib
- Icons from Font Awesome
- Images from Unsplash
