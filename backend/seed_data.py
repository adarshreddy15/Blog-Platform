"""
Database Seed Script - Populate with sample data
Run this after starting the app once to create tables:
    python seed_data.py
"""
from app import create_app
from app.extensions import db
from app.models import User, Post, Tag, Comment
from datetime import datetime, timedelta

app = create_app()

def seed_database():
    with app.app_context():
        # Check if data already exists
        if User.query.first():
            print("Database already has data. Skipping seed.")
            return
        
        print("Seeding database...")
        
        # Create admin user
        admin = User(
            email="admin@blog.com",
            username="admin",
            is_admin=True
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("✓ Created admin user (email: admin@blog.com, password: admin123)")
        
        # Create tags
        tags_data = ["Technology", "Web Development", "Python", "React", "Tutorial", "News"]
        tags = {}
        for name in tags_data:
            tag = Tag(name=name, slug=Tag.generate_slug(name))
            db.session.add(tag)
            tags[name] = tag
        db.session.commit()
        print(f"✓ Created {len(tags)} tags")
        
        # Create sample posts
        posts_data = [
            {
                "title": "Getting Started with React in 2024",
                "content": """<h2>Why React?</h2>
<p>React has become one of the most popular JavaScript libraries for building user interfaces. Its component-based architecture makes it easy to create reusable UI components.</p>

<h2>Key Features</h2>
<ul>
<li><strong>Virtual DOM</strong> - React uses a virtual DOM for efficient updates</li>
<li><strong>JSX</strong> - Write HTML-like syntax in JavaScript</li>
<li><strong>Hooks</strong> - Manage state and side effects in functional components</li>
</ul>

<h2>Getting Started</h2>
<p>To create a new React project, you can use Vite:</p>
<pre><code>npm create vite@latest my-app -- --template react</code></pre>

<p>This will set up a new React project with all the necessary configurations.</p>

<blockquote>React makes it painless to create interactive UIs.</blockquote>""",
                "excerpt": "Learn the fundamentals of React and why it's the go-to choice for modern web development.",
                "tags": ["React", "Web Development", "Tutorial"],
                "status": "published"
            },
            {
                "title": "Building REST APIs with Flask",
                "content": """<h2>Introduction to Flask</h2>
<p>Flask is a lightweight WSGI web application framework in Python. It's designed to make getting started quick and easy, with the ability to scale up to complex applications.</p>

<h2>Creating Your First API</h2>
<p>Here's a simple Flask API example:</p>
<pre><code>from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/hello')
def hello():
    return jsonify({'message': 'Hello, World!'})
</code></pre>

<h2>Best Practices</h2>
<ul>
<li>Use blueprints for organizing routes</li>
<li>Implement proper error handling</li>
<li>Add authentication for protected endpoints</li>
<li>Document your API with Swagger/OpenAPI</li>
</ul>

<p>Flask's simplicity and flexibility make it perfect for building RESTful APIs.</p>""",
                "excerpt": "A comprehensive guide to building RESTful APIs using Python's Flask framework.",
                "tags": ["Python", "Web Development", "Tutorial"],
                "status": "published"
            },
            {
                "title": "The Future of Web Development",
                "content": """<h2>Trends to Watch</h2>
<p>The web development landscape is constantly evolving. Here are some trends shaping the future:</p>

<h3>1. AI-Powered Development</h3>
<p>AI tools are becoming essential for developers, helping with code completion, bug detection, and even generating entire components.</p>

<h3>2. Edge Computing</h3>
<p>Moving computation closer to users for faster response times and better user experience.</p>

<h3>3. Web Components</h3>
<p>Native browser support for reusable components without frameworks.</p>

<h3>4. WebAssembly</h3>
<p>Running high-performance code in the browser, enabling complex applications like games and video editors.</p>

<blockquote>The future of web development is exciting and full of possibilities!</blockquote>""",
                "excerpt": "Explore the emerging trends and technologies that will shape web development in the coming years.",
                "tags": ["Technology", "Web Development", "News"],
                "status": "published"
            },
            {
                "title": "Python Best Practices for Clean Code",
                "content": """<h2>Writing Maintainable Python Code</h2>
<p>Clean code is not just about making things work—it's about making code readable, maintainable, and efficient.</p>

<h2>Key Principles</h2>

<h3>1. Follow PEP 8</h3>
<p>Python's official style guide helps maintain consistency across projects.</p>

<h3>2. Use Type Hints</h3>
<pre><code>def greet(name: str) -> str:
    return f"Hello, {name}!"
</code></pre>

<h3>3. Write Docstrings</h3>
<p>Document your functions and classes for better maintainability.</p>

<h3>4. Keep Functions Small</h3>
<p>Each function should do one thing and do it well.</p>

<h3>5. Use Virtual Environments</h3>
<p>Isolate your project dependencies to avoid conflicts.</p>""",
                "excerpt": "Master the art of writing clean, maintainable Python code with these essential best practices.",
                "tags": ["Python", "Tutorial"],
                "status": "published"
            },
            {
                "title": "Understanding JWT Authentication",
                "content": """<h2>What is JWT?</h2>
<p>JSON Web Token (JWT) is an open standard for securely transmitting information between parties as a JSON object.</p>

<h2>Structure of a JWT</h2>
<p>A JWT consists of three parts:</p>
<ul>
<li><strong>Header</strong> - Contains the token type and signing algorithm</li>
<li><strong>Payload</strong> - Contains the claims (user data)</li>
<li><strong>Signature</strong> - Verifies the token hasn't been tampered with</li>
</ul>

<h2>How It Works</h2>
<ol>
<li>User logs in with credentials</li>
<li>Server validates credentials and generates JWT</li>
<li>Client stores JWT and sends it with each request</li>
<li>Server verifies JWT and grants access</li>
</ol>

<p>JWT is stateless, making it perfect for scalable applications!</p>""",
                "excerpt": "Learn how JWT authentication works and why it's the preferred method for modern web applications.",
                "tags": ["Technology", "Web Development", "Tutorial"],
                "status": "published"
            }
        ]
        
        for i, post_data in enumerate(posts_data):
            post = Post(
                title=post_data["title"],
                slug=Post.generate_slug(post_data["title"]),
                content=post_data["content"],
                excerpt=post_data["excerpt"],
                status=post_data["status"],
                author_id=admin.id,
                published_at=datetime.utcnow() - timedelta(days=len(posts_data) - i),
                created_at=datetime.utcnow() - timedelta(days=len(posts_data) - i)
            )
            for tag_name in post_data["tags"]:
                post.tags.append(tags[tag_name])
            db.session.add(post)
        
        db.session.commit()
        print(f"✓ Created {len(posts_data)} blog posts")
        
        # Create sample comments
        comments_data = [
            {"post_id": 1, "name": "John Doe", "email": "john@example.com", "content": "Great article! Very helpful for beginners.", "status": "approved"},
            {"post_id": 1, "name": "Jane Smith", "email": "jane@example.com", "content": "This helped me understand React better. Thanks!", "status": "approved"},
            {"post_id": 2, "name": "Mike Johnson", "email": "mike@example.com", "content": "Flask is amazing! Can you do a follow-up on Flask-SQLAlchemy?", "status": "approved"},
            {"post_id": 3, "name": "Sarah Wilson", "email": "sarah@example.com", "content": "Excited about the future of web development!", "status": "pending"},
            {"post_id": 4, "name": "Alex Brown", "email": "alex@example.com", "content": "I learned a lot from this. Keep up the great work!", "status": "pending"},
        ]
        
        for comment_data in comments_data:
            comment = Comment(
                post_id=comment_data["post_id"],
                guest_name=comment_data["name"],
                guest_email=comment_data["email"],
                content=comment_data["content"],
                status=comment_data["status"]
            )
            db.session.add(comment)
        
        db.session.commit()
        print(f"✓ Created {len(comments_data)} comments (some pending moderation)")
        
        print("\n✅ Database seeded successfully!")
        print("\n📝 Admin Login:")
        print("   Email: admin@blog.com")
        print("   Password: admin123")

if __name__ == "__main__":
    seed_database()
