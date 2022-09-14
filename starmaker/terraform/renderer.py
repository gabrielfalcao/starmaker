from jinja2 import Environment, PackageLoader, select_autoescape


env = Environment(
    loader=PackageLoader("starmaker.terraform.templates"),
    autoescape=select_autoescape()
)


def render(template_name, **context):
    template = env.get_template(template_name)
    return template.render(**context)
