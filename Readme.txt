Little Lemon Back-End Developer Capstone

GitHub repository:
https://github.com/himanshu91081/courser

API paths for peer testing:

/api/auth/register/
/api/auth/token/
/api/menu-items/
/api/categories/
/api/tables/
/api/bookings/
/api/cart/
/api/orders/
/api/orders/checkout/
/api/orders/{id}/status/

The Django-served HTML landing page is available at:
/

To run locally, install requirements, run `py manage.py migrate`, run
`py manage.py seed_data`, and start the server with `py manage.py runserver`.
The default local database is SQLite. MySQL is supported by setting DB_ENGINE=mysql,
DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, and DB_PORT before migrations.
