"""
File Upload Utilities - Handle image uploads for blog posts
"""
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
from PIL import Image


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(file, subfolder='posts'):
    """
    Save uploaded image to local filesystem.
    
    Args:
        file: FileStorage object from request.files
        subfolder: Subdirectory within uploads folder
    
    Returns:
        str: Relative path to saved image, or None if failed
    """
    if not file or file.filename == '':
        return None
    
    if not allowed_file(file.filename):
        return None
    
    try:
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{extension}"
        
        # Ensure upload directory exists
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        subfolder_path = os.path.join(upload_folder, subfolder)
        os.makedirs(subfolder_path, exist_ok=True)
        
        # Save the file
        filepath = os.path.join(subfolder_path, unique_filename)
        
        # Optionally resize/optimize image
        image = Image.open(file)
        
        # Convert RGBA to RGB if needed (for JPEG)
        if image.mode == 'RGBA' and extension in ['jpg', 'jpeg']:
            image = image.convert('RGB')
        
        # Resize if too large (max 1920px width)
        max_width = 1920
        if image.width > max_width:
            ratio = max_width / image.width
            new_height = int(image.height * ratio)
            image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # Save with optimization
        if extension in ['jpg', 'jpeg']:
            image.save(filepath, 'JPEG', quality=85, optimize=True)
        elif extension == 'png':
            image.save(filepath, 'PNG', optimize=True)
        elif extension == 'webp':
            image.save(filepath, 'WEBP', quality=85)
        else:
            image.save(filepath)
        
        # Return relative path for storage in database
        return f"/uploads/{subfolder}/{unique_filename}"
    
    except Exception as e:
        print(f"Error saving image: {e}")
        return None


def delete_image(image_path):
    """
    Delete an image from the filesystem.
    
    Args:
        image_path: Relative path stored in database (e.g., /uploads/posts/abc.jpg)
    
    Returns:
        bool: True if deleted successfully
    """
    if not image_path:
        return False
    
    try:
        # Convert relative path to absolute
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        # Remove leading /uploads/ from path
        relative_path = image_path.lstrip('/uploads/')
        absolute_path = os.path.join(upload_folder, relative_path)
        
        if os.path.exists(absolute_path):
            os.remove(absolute_path)
            return True
        return False
    
    except Exception as e:
        print(f"Error deleting image: {e}")
        return False
