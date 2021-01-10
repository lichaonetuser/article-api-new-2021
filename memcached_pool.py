# coding=utf8
import memcache
from django.core.signals import request_finished
from django.dispatch import receiver

from api.settings import conf
from pyutil.program import mclb
from pyutil.program.cache import Cache


def get_mc_hosts(conf, hosts, ports):
    host_ports = zip(
        conf.get_values(hosts),
        conf.get_values(ports)
    )
    return ['%s:%s' % (host, port) for host, port in host_ports]


memcache_cli = memcache.Client(
    get_mc_hosts(conf, 'article_memcached_host', 'article_memcached_port'))

cache_lb_memcache_cli = mclb.LBMemcachedClient(
    get_mc_hosts(conf, 'article_lb_memcached_host', 'article_lb_memcached_port'))

static_data_cache = Cache(cache_lb_memcache_cli)


@receiver(request_finished)
def memcached_close_handler(sender, **kwargs):
    # api_logger.info(
    #   'receive a signal disconnect memecahce: %s', memcache_cli)
    memcache_cli.disconnect_all()
