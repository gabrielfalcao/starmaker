from jinja2 import Environment, PackageLoader, select_autoescape


env = Environment(
    loader=PackageLoader(__name__),
    autoescape=select_autoescape()
)
