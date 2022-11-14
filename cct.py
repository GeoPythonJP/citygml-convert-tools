#!/usr/bin/env python
# coding: utf-8

import traceback

import click

import py_plateau
from py_plateau.city_gml import CityGml, Subset


@click.group(help=f"CityGML convert tools (CCT) v{py_plateau.__version__}")
@click.version_option(version=py_plateau.__version__, message="CityGML convert tools (CCT) v%(version)s")
@click.option("-d", "--debug/--no-debug", default=False, help="debug mode")
@click.option("-v", "--verbose", default=False, is_flag=True, help="verbose mode")
@click.pass_context
def main(context, debug, verbose):
    context.obj = dict(debug=debug, verbose=verbose)


@main.command(help="Convert CityGML file to GeoJSON file")
@click.argument("filename", type=click.Path(exists=True))  # input CityGML file name
@click.option("-o", "--output", "output_path", default="output", help="output path name")
@click.option("-s", "--to-srid", "to_srid", default="4326", help="output SRID(EPSG)")
@click.option("-l", "--lod", "lod", default=2, type=click.IntRange(0, 2), help="output lod type")
@click.option("-sp", "--separate", "separate", default=False, is_flag=True, help="separate the building data")
@click.option("-lonlat", "--lonlat", "lonlat", default=True, is_flag=True, help="swap lon lat order")
@click.pass_context
def geojson(context, filename, output_path, to_srid, lod, separate, lonlat):
    """Convert CityGML file to GeoJSON file"""

    try:
        if context.obj["verbose"]:
            click.echo(f"\nConvert CityGML file to GeoJSON file\n")
            click.echo(f" Options:")
            click.echo(f'  debug={context.obj["debug"]}')
            click.echo(f'  verbose={context.obj["verbose"]}')
            click.echo(f"  filename={filename}")
            click.echo(f"  output_path={output_path}")
            click.echo(f"  to_srid={to_srid}")
            click.echo(f"  lod={lod}")
            click.echo(f"  separate={separate}")
            click.echo(f"  lonlat={lonlat}")
            click.echo(f"\n")

        obj_city_gml = CityGml(filename, Subset.GEOJSON, to_srid, separate=separate, lonlat=lonlat)
        if lod == 0:
            obj_city_gml.lod0()
        elif lod == 1:
            obj_city_gml.lod1()
        elif lod == 2:
            obj_city_gml.lod2()
        else:
            raise Exception(f"ERROR: lod number = {lod}")

        obj_city_gml.write_file(output_path)

    except Exception as e:
        click.echo(e)
        traceback.print_exc()


@main.command(help="Convert CityGML file to PLY file")
@click.argument("filename", type=click.Path(exists=True))  # input CityGML file name
@click.option("-o", "--output", "output_path", default="output", help="output path name")
@click.option("-s", "--to-srid", "to_srid", default="6677", help="output SRID(EPSG)")
@click.option("-l", "--lod", "lod", default=2, type=click.IntRange(0, 2), help="output lod type")
@click.option("-sp", "--separate", "separate", default=False, is_flag=True, help="separate the building data")
@click.pass_context
def ply(context, filename, output_path, to_srid, lod, separate):
    """Convert CityGML file to PLY file"""
    try:
        if context.obj["verbose"]:
            click.echo(f"\nConvert CityGML file to PLY file\n")
            click.echo(f" Options:")
            click.echo(f'  debug={context.obj["debug"]}')
            click.echo(f'  verbose={context.obj["verbose"]}')
            click.echo(f"  filename={filename}")
            click.echo(f"  output_path={output_path}")
            click.echo(f"  to_srid={to_srid}")
            click.echo(f"  lod={lod}")
            click.echo(f"  separate={separate}")
            click.echo(f"\n")

        obj_city_gml = CityGml(filename, Subset.PLY, to_srid, separate=separate)
        if lod == 0:
            obj_city_gml.lod0()
        elif lod == 1:
            obj_city_gml.lod1()
        elif lod == 2:
            obj_city_gml.lod2()
        else:
            raise Exception(f"ERROR: lod number = {lod}")

        obj_city_gml.write_file(output_path)

    except Exception as e:
        click.echo(e)
        traceback.print_exc()


if __name__ == "__main__":
    main()
