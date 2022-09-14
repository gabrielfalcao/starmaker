import click
import jinja2
from starmaker.terraform import GCPBootstrapper


@click.group()
@click.option('--debug/--no-debug', default=False)
def main(debug):
    click.echo(f"\tdebug mode is {'on' if debug else 'off'}")


@main.group()
def bootstrap():
    click.echo('\t\tstarmaker bootstrap')


@bootstrap.command()
def gcp():
    click.echo('\t\t\tbootstrapping gcp files')


if __name__ == '__main__':
    main()
