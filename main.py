#!/usr/bin/env python
# coding: utf-8

import argparse
import click
import os
import traceback

import py_plateau
from py_plateau.city_gml import CityGml


@click.group(help=f'citygml convert tools v{py_plateau.__version__}')
@click.version_option(version=py_plateau.__version__, message="citygml convert tools v%(version)s")
@click.option('--debug/--no-debug', default=False)
@click.option('--verbose', default=False, is_flag=True)
@click.pass_context
def main(context, debug, verbose):
    context.obj = dict(debug=debug, verbose=verbose)


@main.command(help='Convert CityGML file to PLY file')
@click.argument('filename', type=click.Path(exists=True))   # input CityGML file name
@click.option('-o', '--output', 'output_path', default='output', help='output path name')
@click.option('-s', '--to-srid', 'to_srid', default='6677', help='output SRID(EPSG)')
@click.option('-l', '--lod', 'lod', default=2, type=click.IntRange(0, 2), help='output lod type')
@click.pass_context
def ply(context, filename, output_path, to_srid, lod):

    try:
        if context.obj["verbose"]:
            click.echo(f'\nConvert CityGML file to PLY file\n')
            click.echo(f' Options:')
            click.echo(f'  debug={context.obj["debug"]}')
            click.echo(f'  verbose={context.obj["verbose"]}')
            click.echo(f'  filename={filename}')
            click.echo(f'  output_path={output_path}')
            click.echo(f'  to_srid={to_srid}')
            click.echo(f'  lod={lod}')
            click.echo(f'\n')

        obj_city_gml = CityGml(filename, to_srid)
        if lod == 0:
            obj_city_gml.lod0()
        elif lod == 1:
            obj_city_gml.lod1()
        elif lod == 2:
            obj_city_gml.lod2()
        else:
            raise Exception(f"ERROR: lod number = {lod}")

        os.makedirs(output_path, exist_ok=True)
        obj_city_gml.write_ply(output_path)

    except Exception as e:
        print(e)
        traceback.print_exc()


if __name__ == "__main__":
    main()