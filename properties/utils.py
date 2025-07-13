from django.core.cache import cache
from .models import Property

def get_all_properties():
    properties = cache.get('all_properties')
    if not properties:
        properties = list(Property.objects.all().values('id', 'title', 'description', 'price', 'location', 'created_at'))
        cache.set('all_properties', properties, 3600)  # cache for 1 hour
    return properties

import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    redis_conn = get_redis_connection("default")  # Use your configured Redis cache alias
    
    info = redis_conn.info()  # Get all Redis INFO stats
    
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    
    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0.0
    
    metrics = {
        "keyspace_hits": hits,
        "keyspace_misses": misses,
        "hit_ratio": hit_ratio,
    }
    
    logger.info(f"Redis Cache Metrics: Hits={hits}, Misses={misses}, Hit Ratio={hit_ratio:.2f}")
    
    return metrics
