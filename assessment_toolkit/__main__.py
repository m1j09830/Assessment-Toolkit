#Created by Miguel Rios
import typer
from enum import Enum
from pathlib import Path
from assessment_toolkit.logger import init_logger, logger, console
from assessment_toolkit import __version__
from assessment_toolkit.lib.cool_scans import *

app = typer.Typer(
    add_completion=False,
    rich_markup_mode='rich',
    context_settings={'help_option_names': ['-h', '--help']},
    pretty_exceptions_show_locals=False
)

class Operations(str, Enum):
    scoper = "scoper"
    shodan_scans = "shodan_scans"
    discovery = "discovery"
    full = "full"
    nikto = "nikto"
    aquatone = "aquatone"
    internal_scans = "internal_scans"
    external_scans = "external_scans"
    nuclei_scans = "nuclei_scans"
    backup = "backup"

@app.command(no_args_is_help=True, help='Assessment-Toolkit help!')
def main(
    operation: Operations = typer.Option(..., '--operation', '-o', 
        help='Operation to be run'),
    project_name: str = typer.Option(..., '--project-name', '-p', help='Set project name'),
    input_file: Path = typer.Option(
        ..., '--input-file', '-i', exists=True, file_okay=True, dir_okay=False, 
        readable=True, help='Set input file'),
    exclude_file: Path = typer.Option(
        None, '--exclude-file', '-e', exists=True, file_okay=True, dir_okay=False, 
        readable=True, help='Set exclude file. NOTE: Only for scoper function'),
    debug: bool = typer.Option(False, '--debug', help='Enable [green]DEBUG[/] output')):

    init_logger(debug)
    input_file=str(input_file)
    if exclude_file:
        exclude_file=str(exclude_file)
    else:
        exclude_file=None

    if operation == Operations.scoper:
        scoper(project_name, input_file, exclude_file)
    
    if operation == Operations.discovery:
        discovery(project_name, input_file)
    
    if operation == Operations.full:
        full_port(project_name, input_file)

    if operation == Operations.nikto:
        nikto(project_name, input_file)

    if operation == Operations.aquatone:
        aquatone(project_name, input_file)

    if operation == Operations.external_scans:
        external_scans(project_name, input_file)

    if operation == Operations.internal_scans:
        internal_scans(project_name, input_file)
    
    if operation == Operations.shodan_scans:
        shodan_scans(project_name, input_file)

    if operation == Operations.nuclei_scans:
        nuclei_scans(project_name, input_file)

if __name__ == '__main__':
    app(prog_name='Assessment-Toolkit')
