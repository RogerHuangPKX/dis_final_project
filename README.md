# Enterprise Data System

A comprehensive enterprise data management system built with Django and Vue.js, featuring customer management, contract handling, and analytics capabilities.

## Features

- User Authentication
- Customer Management (CRUD operations)
- Contract Management
- Insurance Quote Generation
- Risk Analysis
- Analytics Dashboard
- Responsive Design

## Tech Stack

### Backend
- Python 3.10
- Django 4.2
- Django REST Framework
- PostgreSQL
- JWT Authentication

### Frontend
- Vue.js 3
- TypeScript
- Element Plus UI
- ECharts
- Axios

## Prerequisites

- Docker
- Docker Compose

## Quick Start

### Using start script (Recommended)
```bash
git clone <repository-url>
cd enterprise_data_system_final
./start.sh
```

The script will automatically:
1. Create the .env file if it doesn't exist
2. Build and start the containers
3. Run database migrations
4. Create a superuser account
5. Generate test data

### Manual Setup
If you prefer to set up manually, follow these steps:

1. Clone the repository:
```bash
git clone <repository-url>
cd enterprise_data_system_final
```

2. Create a `.env` file in the root directory with the following content:
```env
POSTGRES_DB=enterprise_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
```

3. Build and start the containers:
```bash
docker compose up --build -d
```

4. Run migrations:
```bash
docker compose exec backend python manage.py migrate
```

5. Create a superuser account:
```bash
docker compose exec backend python manage.py createsuperuser
```

6. Generate test data:
```bash
docker compose exec backend python manage.py generate_test_data
```

## Docker Image Publishing

### Using publish script (Recommended)

1. Create repositories on Docker Hub:
   - Go to https://hub.docker.com/
   - Click "Create Repository" button
   - Create two repositories: `enterprise-frontend` and `enterprise-backend`
   - Make them public if you want others to be able to pull them

2. Run the publish script:
```bash
./publish.sh your-username
```
Replace `your-username` with your Docker Hub username.

The script will automatically:
- Check if Docker is installed
- Log you into Docker Hub
- Tag the images with your username
- Push the images to Docker Hub

### Manual Publishing

If you prefer to publish manually:

1. Login to Docker Hub:
```bash
docker login
```
Enter your Docker Hub username and password when prompted.

2. Tag the images:
```bash
# Get the image IDs
docker images

# Tag the images with your Docker Hub username
docker tag <frontend-image-id> your-username/enterprise-frontend:latest
docker tag <backend-image-id> your-username/enterprise-backend:latest
```

3. Push the images:
```bash
docker push your-username/enterprise-frontend:latest
docker push your-username/enterprise-backend:latest
```

Note: Replace `your-username` with your actual Docker Hub username.

To use the published images:

1. Update docker-compose.yml:
```yaml
services:
  frontend:
    image: your-username/enterprise-frontend:latest
    ...
  backend:
    image: your-username/enterprise-backend:latest
    ...
```

2. Pull and run:
```bash
docker compose pull
docker compose up -d
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api
- Admin Interface: http://localhost:8000/admin

## Project Structure

```
enterprise_data_system/
├── backend/                 # Django backend
│   ├── core/               # Main application
│   │   ├── models/         # Database models
│   │   ├── views.py        # API views
│   │   └── serializers.py  # API serializers
│   └── manage.py
├── frontend/               # Vue.js frontend
│   ├── src/
│   │   ├── views/         # Vue components
│   │   ├── api/           # API integration
│   │   └── router/        # Route configuration
│   └── package.json
└── docker-compose.yml      # Docker configuration
```

## API Endpoints

### Authentication
- POST `/auth/login/` - User login
- POST `/auth/refresh/` - Refresh JWT token

### Customers
- GET `/api/customers/` - List customers
- POST `/api/customers/` - Create customer
- GET `/api/customers/{id}/` - Get customer details
- PUT `/api/customers/{id}/` - Update customer
- DELETE `/api/customers/{id}/` - Delete customer
- GET `/api/customers/{id}/risk-analysis/` - Get customer risk analysis

### Contracts
- GET `/api/contracts/` - List contracts
- POST `/api/contracts/` - Create contract
- GET `/api/contracts/{id}/` - Get contract details
- PUT `/api/contracts/{id}/` - Update contract
- DELETE `/api/contracts/{id}/` - Delete contract
- GET `/api/contracts/analytics/` - Get contract analytics

### Quotes
- POST `/api/quotes/calculate/` - Calculate insurance quote
- POST `/api/quotes/accept/` - Accept quote

## Development

### Backend Development
```bash
# Run migrations
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate

# Create superuser
docker compose exec backend python manage.py createsuperuser

# Generate test data
docker compose exec backend python manage.py generate_test_data
```

### Frontend Development
```bash
# Install dependencies
cd frontend/vue-project
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## Testing

```bash
# Run backend tests
docker compose exec backend python manage.py test

# Run frontend tests
cd frontend/vue-project
npm run test
```

## Default Users

After running the test data generation command, the following users will be available:

- Admin User:
  - Username: admin
  - Password: Admin@123456

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Jinze Huang (jh9108)
