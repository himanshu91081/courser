# Little Lemon Backend API

A Django REST Framework backend for the Little Lemon restaurant capstone. It includes token authentication, role-based permissions, menu management, bookings, customer carts, checkout, orders, and delivery-status operations.

## Features

- Customer registration and DRF token login
- Manager, Delivery crew, and Customer groups
- Manager-only menu/category/table management
- Public-to-authenticated users read-only menu access with search, category, featured, ordering, and pagination
- Customer-owned bookings and order history
- Per-user cart and atomic checkout
- Manager/delivery crew order-status updates
- Django admin and seed data command
- Automated API workflow tests

## Run locally

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py seed_data
py manage.py test
py manage.py runserver
```

API base URL: `http://127.0.0.1:8000/api/`

## Authentication

Register: `POST /api/auth/register/`

```json
{"username":"alice","email":"alice@example.com","password":"securepass123"}
```

Get token: `POST /api/auth/token/`

```json
{"username":"alice","password":"securepass123"}
```

Use the returned token on protected requests:

```text
Authorization: Token <token>
```

## Demo accounts

After `seed_data`, the accounts are `manager`, `delivery`, and `customer`. The demo password is `LittleLemon123!`. Change or remove these accounts before deploying anywhere public.

## Main endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/register/` | Register a customer |
| POST | `/api/auth/token/` | Obtain a token |
| GET/POST/PATCH/DELETE | `/api/menu-items/` | Browse or manage menu items |
| GET/POST | `/api/bookings/` | Manage the authenticated customer's bookings |
| GET/POST | `/api/cart/` | View or add cart items |
| POST | `/api/orders/checkout/` | Convert the current cart into an order |
| GET | `/api/orders/` | View customer or staff orders |
| PATCH | `/api/orders/{id}/status/` | Staff update delivery status |

## GitHub submission checklist

1. Push this repository to a public GitHub repository.
2. Submit the repository URL in the Coursera peer-review form.
3. Include screenshots showing registration/login, customer menu access, manager menu creation, booking creation, cart checkout, and staff order-status update.
4. Do not include `db.sqlite3`, tokens, API keys, or private credentials.
