# Blog Platform with Admin Panel

A full-stack blog application built with React.js and Flask.
[▶ Watch Demo Video](assets/demo.mp4)

## Features

### Public Features
- 📜 **Home Page**: Browse the latest articles from all authors.
- 🏷️ **Tag Filtering**: Explore content categorized by specific topics.
- 💬 **Interactive Comments**: Engage with posts as a guest or registered user.
- 📡 **RSS Support**: Stay updated with the latest posts via the public RSS feed.

### Unified User Portal (New)
The user portal has been completely redesigned with a **Unified Sidebar Layout** matching the Admin Panel for a seamless experience.
- � **Dashboard**: High-level overview of your contributions and stats.
- 📝 **Post Management**: Create, edit, and delete your own articles with a professional UI.
- ✏️ **Rich Content**: Compose posts using a powerful rich text editor with image support.
- 💬 **Comment Control**: View and manage all the comments you've left across the platform.
- 🏠 **Smart Navigation**: Persistent sidebar for quick access with consistent backtracking (e.g., "Back to My Posts").

### Admin Panel
- 🔐 **Secure Access**: Requires a unique admin registration code for initialization.
- 👥 **User Moderation**: View and manage all platform users.
- �️ **Global Content Control**: Edit or delete any post or comment on the platform.
- � **Platform Insights**: Comprehensive statistics for the entire blog platform.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React.js (Vite) |
| Backend | Python (Flask) |
| Database | PostgreSQL (SQLite for development) |
| Auth | JWT |
| Rich Editor | React Quill |

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.8+
- PostgreSQL (optional, SQLite works for development)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
copy .env.example .env
# Edit .env with your settings

# Run the server
python run.py
```

Backend will be available at: `http://localhost:5000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## Configuration

### Backend Environment Variables (.env)

Create a `.env` file in the `backend` directory based on `.env.example`:

```env
# Database (SQLite works out of the box)
DATABASE_URL=sqlite:///blog.db

# For PostgreSQL:
# DATABASE_URL=postgresql://username:password@localhost:5432/blog_db

# JWT Secret (change in production!)
JWT_SECRET_KEY=your-super-secret-jwt-key

# Flask
SECRET_KEY=your-flask-secret-key
FLASK_ENV=development

# Admin Registration Code
# IMPORTANT: Change this to a strong secret code in production!
# Users must provide this code to register as admin
ADMIN_REGISTRATION_CODE=ADMIN_SECRET_CODE_123
```

### Admin Code Setup

The `ADMIN_REGISTRATION_CODE` is a special secret code required to register admin accounts. This prevents unauthorized users from creating admin accounts.

**To register as admin:**
1. Set your secret admin code in the `.env` file
2. Use the `/api/auth/admin/register` endpoint with the admin code
3. The code is validated server-side before creating admin accounts

**Security Note:** Keep this code secret and change it from the default value in production!

## API Endpoints

### Public Endpoints
- `GET /api/posts` - List published posts
- `GET /api/posts/:slug` - Get single post
- `GET /api/posts/tags` - Get all tags
- `GET /api/posts/tags/:slug` - Filter by tag
- `POST /api/posts/:id/comments` - Submit guest comment
- `GET /api/rss` - RSS feed

### Authentication Endpoints

#### User Registration & Login
- `POST /api/auth/register` - Register as regular user
  ```json
  {
    "email": "user@example.com",
    "username": "user",
    "password": "password123"
  }
  ```
- `POST /api/auth/login` - Login as user (returns JWT token)
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```

#### Admin Registration & Login (Requires Special Code)
- `POST /api/auth/admin/register` - Register as admin (requires admin_code)
  ```json
  {
    "email": "admin@example.com",
    "username": "admin",
    "password": "password123",
    "admin_code": "ADMIN_SECRET_CODE_123"
  }
  ```
- `POST /api/auth/admin/login` - Login as admin (returns JWT token)
  ```json
  {
    "email": "admin@example.com",
    "password": "password123"
  }
  ```

### User Endpoints (JWT Required - Regular Users)
All user endpoints require `Authorization: Bearer <JWT_TOKEN>` header

#### User Dashboard
- `GET /api/user/dashboard` - Get user stats and info

#### User Posts Management
- `GET /api/user/posts` - List user's own posts
- `GET /api/user/posts/:id` - Get specific user post
- `POST /api/user/posts` - Create new post
- `PUT /api/user/posts/:id` - Update own post
- `DELETE /api/user/posts/:id` - Delete own post
- `POST /api/user/posts/upload` - Upload image for post

#### User Comments Management
- `GET /api/user/comments` - List user's own comments
- `POST /api/user/posts/:id/comments` - Create comment on post
- `PUT /api/user/comments/:id` - Update own comment
- `DELETE /api/user/comments/:id` - Delete own comment

### Admin Endpoints (JWT Required - Admin Only)
All admin endpoints require `Authorization: Bearer <JWT_TOKEN>` header with admin privileges

#### Admin Dashboard
- `GET /api/admin/dashboard` - Get admin dashboard statistics

#### Posts Management (Admin)
- `GET /api/admin/posts` - List all posts (including drafts)
- `GET /api/admin/posts/:id` - Get any post by ID
- `POST /api/admin/posts` - Create post
- `PUT /api/admin/posts/:id` - Update any post
- `DELETE /api/admin/posts/:id` - Delete any post
- `POST /api/admin/posts/upload` - Upload image

#### Comments Management (Admin)
- `GET /api/admin/comments` - List all comments with filters
- `PUT /api/admin/comments/:id` - Moderate comment (approve/reject)
- `DELETE /api/admin/comments/:id` - Delete any comment

#### User Management (Admin Only)
- `GET /api/admin/users` - List all users
- `GET /api/admin/users/:id` - Get user details
- `DELETE /api/admin/users/:id` - Delete user and their content
- `GET /api/admin/users/:id/posts` - Get all posts by specific user
- `PUT /api/admin/users/:id/posts/:post_id` - Update any user's post
- `DELETE /api/admin/users/:id/posts/:post_id` - Delete any user's post
- `GET /api/admin/users/:id/comments` - Get all comments by specific user

## API Testing

Import `Blog_Platform_API.postman_collection.json` into Postman or Hoppscotch to test all endpoints.

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── __init__.py      # App factory (IoC)
│   │   ├── config.py
│   │   ├── extensions.py
│   │   ├── models/          # Database models
│   │   ├── services/        # Business logic (IoC)
│   │   ├── routes/          # API endpoints
│   │   └── utils/
│   ├── uploads/             # Image storage
│   ├── requirements.txt
│   └── run.py
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── layout/      # Header, Footer
    │   │   ├── blog/        # PostCard, Comments
    │   │   └── admin/       # AdminLayout
    │   ├── pages/
    │   │   ├── HomePage.jsx
    │   │   ├── PostPage.jsx
    │   │   └── admin/       # Admin pages
    │   ├── services/        # API calls
    │   ├── context/         # Auth context
    │   └── App.jsx
    └── package.json
```

## Design Patterns

### Inversion of Control (IoC)

The backend uses IoC for loose coupling:
- **App Factory Pattern**: Flask app is created via `create_app()` function
- **Service Layer**: Business logic is separated from routes
- **Dependency Injection**: Extensions are injected into the app

## License

MIT License

