from pkg_resources import DistributionNotFound, get_distribution


try:
    __version__ = get_distribution("forked-flake8-cached").version
except DistributionNotFound:
    __version__ = "(local)"
