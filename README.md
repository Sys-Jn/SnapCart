# SnapCart — Curated Essentials E-Commerce Platform

A full-stack e-commerce web application built with Flask, featuring Razorpay payment integration and automated deployment on AWS Elastic Beanstalk via GitHub Actions CI/CD.

---

## Live Demo

🌐 **[snapcart-env-1.eba-mtgnvqhk.eu-north-1.elasticbeanstalk.com](http://snapcart-env-1.eba-mtgnvqhk.eu-north-1.elasticbeanstalk.com/)**

---

## Screenshots

> *(Add screenshots of homepage, product page, cart, and checkout here)*

---

## Features

- **Product Catalog** — 13 curated products with search, category filtering, and popularity filters
- **User Authentication** — Register, login, logout with hashed passwords via Werkzeug
- **Shopping Cart** — Session-based cart with quantity management and order summary
- **Product Detail Pages** — Individual product pages with related product suggestions
- **Razorpay Payment Gateway** — Real payment integration with HMAC signature verification
- **Order Management** — Order creation, payment tracking, and success confirmation
- **Responsive Design** — Mobile-friendly UI with Playfair Display + DM Sans typography
- **CI/CD Pipeline** — Auto-deploy to AWS on every GitHub push via GitHub Actions

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, Flask 3.x |
| Database | SQLite (dev) |
| ORM | Flask-SQLAlchemy 3.x |
| Auth | Flask-Login, Werkzeug |
| Payments | Razorpay SDK |
| Frontend | Jinja2, Vanilla JS, CSS3 |
| Deployment | AWS Elastic Beanstalk (eu-north-1) |
| CI/CD | GitHub Actions |

---

## Project Structure

```
SnapCart/
├── main.py                  # Flask app, routes, payment logic
├── models.py                # SQLAlchemy models (User, Product, Order)
├── application.py           # AWS Beanstalk entry point
├── Procfile                 # Gunicorn start command
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── .github/
│   └── workflows/
│       └── deploy.yml       # GitHub Actions CI/CD pipeline
├── static/
│   └── css/
│       └── style.css        # All styles
└── templates/
    ├── base.html            # Navbar, footer, flash messages
    ├── index.html           # Homepage with hero, categories, products
    ├── product.html         # Product detail + related products
    ├── cart.html            # Cart page with order summary
    ├── checkout.html        # Razorpay checkout integration
    ├── order_success.html   # Post-payment confirmation
    ├── login.html           # Login page
    └── register.html        # Registration page
```

---

## Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/Sys-Jn/SnapCart.git
cd SnapCart
```

### 2. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:
```
SECRET_KEY=your-secret-key-here
RAZORPAY_KEY_ID=rzp_test_xxxx
RAZORPAY_KEY_SECRET=your_secret_here
DATABASE_URL=sqlite:///store.db
```

> Get free Razorpay test keys at [dashboard.razorpay.com](https://dashboard.razorpay.com)

### 5. Run the app
```bash
python main.py
```

Visit `http://localhost:5000`

---

## Database Models

```
User          — id, name, email, password (hashed)
Product       — id, name, description, price, image_url, category, is_popular, stock
Order         — id, user_id, razorpay_order_id, razorpay_payment_id, total, status
```

---

## Payment Flow

```
User clicks Checkout
      ↓
Flask creates Razorpay order (server-side)
      ↓
Razorpay checkout modal opens (client-side)
      ↓
User pays → Razorpay sends payment_id + signature
      ↓
Flask verifies HMAC signature (server-side)
      ↓
Order status updated to 'paid' → cart cleared → success page
```

---

## Deployment (AWS Elastic Beanstalk)

This project uses GitHub Actions for automated deployment. Every push to `main` branch triggers a deploy to AWS Elastic Beanstalk.

### CI/CD Flow

```
Push to GitHub (main branch)
        ↓
GitHub Actions workflow triggers
        ↓
Code zipped and uploaded to AWS S3
        ↓
Elastic Beanstalk deploys new version
        ↓
Live website updates automatically
```

### Required GitHub Secrets

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user access key |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |
| `AWS_REGION` | `eu-north-1` |
| `AWS_EB_APP_NAME` | `SnapCart` |
| `AWS_EB_ENV_NAME` | `SnapCart-env-1` |

### Deploy
```bash
git add .
git commit -m "your changes"
git push origin main
# GitHub Actions handles the rest automatically
```

---

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `SECRET_KEY` | Flask session secret | Yes |
| `RAZORPAY_KEY_ID` | Razorpay public key | Yes |
| `RAZORPAY_KEY_SECRET` | Razorpay secret key | Yes |
| `DATABASE_URL` | Database connection string | Yes |

---

## Author

Sanyam Jain

---

