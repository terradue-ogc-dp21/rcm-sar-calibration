import os
import sys
import logging
import click
from .stac import get_item
from .factory import read_ml, ml_db, ml_sf

logging.basicConfig(
    stream=sys.stderr,
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)


@click.command(
    short_help="RCM SAR Calibration",
    help="This service provides calibrated products from input radar EO data. The output products, such as the calibrated backscatter coefficient in dB, can be used as input for further thematic processing (e.g. co-location, flood mapping).",
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    ),
)
@click.option(
    "--input_path",
    "-i",
    "input_path",
    help="Path to an RCM SAR acquisition staged as a STAC catalog",
    type=click.Path(),
    required=True,
)
@click.pass_context
def main(ctx, input_path):

    item = get_item(os.path.join(input_path, "catalog.json"))

    read_ml(item)

    ml_db(item)

    ml_sf(item)

    sys.exit(0)

if __name__ == "__main__":
    main()