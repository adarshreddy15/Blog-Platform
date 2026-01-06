from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.post import Post
from datetime import datetime

app = create_app()
app.app_context().push()

# Get admin user
admin = User.query.filter_by(is_admin=True).first()
if not admin:
    print('No admin found, creating one...')
    admin = User(email='admin@blog.com', username='admin', is_admin=True)
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()

# Create sample posts
posts_data = [
    {
        'title': 'Getting Started with Flask and React',
        'slug': 'getting-started-flask-react',
        'content': 'Flask is a lightweight WSGI web application framework in Python, while React is a JavaScript library for building user interfaces. Flask is simple and easy to learn, flexible and unopinionated, great for building APIs, and has an extensive ecosystem. React provides a component-based architecture, virtual DOM for performance, rich ecosystem, and great developer experience. Together, they make a powerful stack for modern web applications!',
        'excerpt': 'Learn how to build modern web applications using Flask backend and React frontend.',
        'tags': ['flask', 'react', 'python', 'javascript'],
        'status': 'published'
    },
    {
        'title': 'Understanding PostgreSQL Database',
        'slug': 'understanding-postgresql-database',
        'content': 'PostgreSQL is a powerful, open source object-relational database system with ACID compliance, advanced data types, full-text search, JSON support, and extensibility. It is reliable, performant, standards-compliant, and backed by a strong open-source community. PostgreSQL is perfect for production applications!',
        'excerpt': 'Explore the features and benefits of PostgreSQL database system.',
        'tags': ['postgresql', 'database', 'sql'],
        'status': 'published'
    },
    {
        'title': 'JWT Authentication Best Practices',
        'slug': 'jwt-authentication-best-practices',
        'content': 'JSON Web Tokens (JWT) are a compact, URL-safe means of representing claims between two parties. Security best practices include using strong secret keys, setting appropriate expiration times, storing tokens securely, validating tokens properly, and using HTTPS in production. Never store sensitive data in JWT payload, implement token refresh mechanism, add role-based access control, and handle token expiration gracefully. Stay secure!',
        'excerpt': 'Learn best practices for implementing JWT authentication in your applications.',
        'tags': ['jwt', 'security', 'authentication'],
        'status': 'published'
    },
    {
        'title': 'Building RESTful APIs with Flask',
        'slug': 'building-restful-apis-flask',
        'content': 'REST (Representational State Transfer) is an architectural style for designing networked applications. REST principles include client-server architecture, stateless communication, cacheable responses, and uniform interface. Best practices for Flask APIs include using proper HTTP methods, returning appropriate status codes, versioning your API, and documenting with Swagger/OpenAPI. Build scalable APIs!',
        'excerpt': 'A comprehensive guide to building RESTful APIs using Flask framework.',
        'tags': ['flask', 'api', 'rest', 'python'],
        'status': 'published'
    },
    {
        'title': 'React Hooks Complete Guide',
        'slug': 'react-hooks-complete-guide',
        'content': 'React Hooks let you use state and other React features without writing a class. Common hooks include useState for managing component state, useEffect for handling side effects, useContext for accessing context values, and useRef for referencing DOM elements. You can create custom hooks to reuse stateful logic. Benefits include simpler code, better reusability, easier testing, and no more class confusion. Happy coding!',
        'excerpt': 'Master React Hooks and write better functional components.',
        'tags': ['react', 'javascript', 'hooks', 'frontend'],
        'status': 'published'
    }
]

# Add posts
from app.models.post import Tag

for post_data in posts_data:
    existing = Post.query.filter_by(slug=post_data['slug']).first()
    if not existing:
        post = Post(
            title=post_data['title'],
            slug=post_data['slug'],
            content=post_data['content'],
            excerpt=post_data['excerpt'],
            status=post_data['status'],
            author_id=admin.id,
            published_at=datetime.utcnow()
        )

        # Add tags
        for tag_name in post_data['tags']:
            tag_slug = Tag.generate_slug(tag_name)
            tag = Tag.query.filter_by(slug=tag_slug).first()
            if not tag:
                tag = Tag(name=tag_name, slug=tag_slug)
                db.session.add(tag)
            post.tags.append(tag)

        db.session.add(post)
        print(f'Added post: {post.title}')
    else:
        print(f'Post already exists: {post_data["title"]}')

db.session.commit()
print(f'\nTotal posts in database: {Post.query.count()}')
print('Sample posts added successfully!')
