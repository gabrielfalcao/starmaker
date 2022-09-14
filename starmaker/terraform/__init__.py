from pathlib import Path
from starmaker.terraform.templates.gcp import jinja2_env

class Bootstraper(object):

    templates = (
        ('main', 'main.tf.j2'),
        ('variables', 'variables.tf.j2'),
        ('outputs', 'outputs.tf.j2'),
    )

    def __init__(self, path: Path):
        self.output_path = path

    def iter_templates(self):
        for name, src in self.templates:
            yield (name, src, self.env.get_template(src))

    def iter_render(self, **context):
        for name, src, template in self.iter_templates():
            rendered = template.render(template_name=name, template_src=src, **context)
            yield (name, src, template, rendered)




class GCPBootstrapper(Bootstraper):
    env = jinja2_env
