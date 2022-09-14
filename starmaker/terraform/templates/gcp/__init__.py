from jinja2 import Environment, PackageLoader


jinja2_env = Environment(
    loader=PackageLoader(__name__),
)

__all__ = ['jinja2_env']
