from beaker.cache import CacheManager, Cache
from beaker.util import parse_cache_config_options

DEFAULT_EXPIRE = 300

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': './cache/data',
    'cache.lock_dir': './cache/lock'
}

cache_manager = CacheManager(**parse_cache_config_options(cache_opts))
