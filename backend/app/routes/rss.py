"""
RSS Feed Route - Generate RSS feed for blog
"""
from flask import Blueprint, Response, request
from ..services import rss_service

rss_bp = Blueprint('rss', __name__)


@rss_bp.route('/rss', methods=['GET'])
def get_rss_feed():
    """
    Get RSS 2.0 feed for published blog posts.
    
    Returns XML content type.
    """
    # Get base URL from request or use default
    base_url = request.host_url.rstrip('/')
    
    feed_xml = rss_service.generate_feed(base_url=base_url)
    
    return Response(feed_xml, mimetype='application/rss+xml')


@rss_bp.route('/rss/info', methods=['GET'])
def get_rss_info():
    """Get information about the RSS feed"""
    base_url = request.host_url.rstrip('/')
    info = rss_service.get_feed_info(base_url=base_url)
    
    return info, 200
