import glob
import os
import os.path
import shutil
import sys
from pathlib import Path

import click

cwd = Path(__file__).resolve().parent

librarys = [
    'ej2',
    'ej2-barcode-generator',
    'ej2-base',
    'ej2-buttons',
    'ej2-calendars',
    'ej2-charts',
    'ej2-circulargauge',
    'ej2-compression',
    'ej2-data',
    'ej2-diagrams',
    'ej2-documenteditor',
    'ej2-drawings',
    'ej2-dropdowns',
    'ej2-excel-export',
    'ej2-file-utils',
    'ej2-filemanager',
    'ej2-gantt',
    'ej2-grids',
    'ej2-heatmap',
    'ej2-image-editor',
    'ej2-inplace-editor',
    'ej2-inputs',
    'ej2-kanban',
    'ej2-layouts',
    'ej2-lineargauge',
    'ej2-lists',
    'ej2-maps',
    'ej2-navigations',
    'ej2-notifications',
    'ej2-office-chart',
    'ej2-pdf',
    'ej2-pdf-export',
    'ej2-pdfviewer',
    'ej2-pivotview',
    'ej2-popups',
    'ej2-progressbar',
    'ej2-querybuilder',
    'ej2-ribbon',
    'ej2-richtexteditor',
    'ej2-schedule',
    'ej2-splitbuttons',
    'ej2-spreadsheet',
    'ej2-svg-base',
    'ej2-treegrid',
    'ej2-treemap',
]


@click.command()
@click.option('-d', '--directory', required=True, prompt='Directory', help='Directory To Walk All Library')
def command(directory, ):
    '''Syncfusion Collector, By ©Tukang Pecut Juru Ketik™ @ IT.Nusantara Group'''
    click.echo(f'''{click.style(f'Note: please edit', fg='blue', bold=True)} {click.style('pdfviewer.min.js:ej2Pdf', fg='green', bold=True)} To {click.style('pdfviewer.min.js:ej.pdf', fg='red', blink=True)} {click.style(f'before pack.py', fg='blue', bold=True)}''')
    directory = directory.replace('\\', '/')
    directory = f'{directory}/' if not directory.endswith('/') else directory
    for library in librarys:
        input = os.path.join(directory, library, 'dist/global', f'{library}.min.js')
        if not os.path.exists(input):
            input = os.path.join(directory, library, 'dist', f'{library}.min.js')
        output = os.path.join(cwd, 'vendor/syncfusion/js', f'{library.replace('ej2', 'all').replace('all-', '').replace('-', '')}.min.js')
        if not os.path.exists(os.path.dirname(output)):
            os.makedirs(os.path.dirname(output))
        click.echo(f'''{click.style(f'Copy', fg='blue', bold=True)} {click.style(input, fg='green', bold=True)} To {click.style(output, fg='red', blink=True)}''')
        shutil.copyfile(input, output)
        content = open(output, 'r', encoding='utf8')
        recontent = []
        for line in content.readlines():
            if not any(find in line.strip() for find in ['//# sourceMappingURL=', ]):
                recontent.append(line)
        content.close()
        content = open(output, 'w', encoding='utf8')
        content.writelines(recontent)
        content.close()
        inputs = glob.iglob(os.path.join(os.path.join(directory, library, 'styles'), '*.css'), recursive=False)
        if not any(inputs):
            inputs = glob.iglob(os.path.join(os.path.join(directory, library), '*.css'), recursive=False)
        if not any(inputs):
            click.echo(f'''{click.style(f'Skipped', fg='red', bold=True)} {click.style(os.path.join(directory, library), fg='green', bold=True)} {click.style('Not Contains *.css', fg='red', blink=True)}''')
        for input in inputs:
            output = os.path.join(cwd, 'vendor/syncfusion/css', f'{library.replace('ej2', 'all').replace('all-', '').replace('-', '')}', os.path.basename(input))
            if not os.path.exists(os.path.dirname(output)):
                os.makedirs(os.path.dirname(output))
            click.echo(f'''{click.style(f'Copy', fg='blue', bold=True)} {click.style(input, fg='green', bold=True)} To {click.style(output, fg='red', blink=True)}''')
            shutil.copyfile(input, output)


if __name__ == '__main__':
    if sys.stdin and sys.stdin.isatty():
        os.system('cls' if os.name == 'nt' else 'clear')
    command()
