"""Create new Avanza Stock Sensors."""

import click
from string import Template

TEMPLATE_FILE = "avanza_stock.yaml.template"

@click.command()
@click.argument('name', type=click.STRING)
@click.argument('id', type=click.INT)
def cli(name, id):
    """Create new Avanza Stock Sensors.

    NAME: The name of the stock.\n
    ID: The Avanza id of the stock. Obtainable via the URL.
    """
    filein = open( TEMPLATE_FILE )
    template = Template( filein.read() )
    result = template.safe_substitute(name=name,id=id)
    filename = f"avanza_stock_{name}.yaml"
    with open(filename, "w") as f:
        f.write(result)

if __name__ == '__main__':
    cli()