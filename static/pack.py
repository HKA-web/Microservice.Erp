import base64
import io
import os
import os.path
import shutil
import sys
import zipfile
from datetime import datetime

import click


def format(bytes, suffix='B', ):
    factor = 1024
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < factor:
            return f'{bytes:.2f} {unit}{suffix}'
        bytes /= factor


@click.command()
@click.option('-d', '--directory', required=True, prompt='Directory', help='Directory To Walk All JavaScript')
@click.option('-c', '--compression', default=9, help='Compression Level 0 - 9')
def command(directory, compression):
    '''JavaScript Packer For Reduct Size, By ©Tukang Pecut Juru Ketik™ @ IT.Nusantara Group'''
    directory = directory.replace('\\', '/')
    directory = f'{directory}/' if not directory.endswith('/') else directory
    copyright = f'''Packed By ©Tukang Pecut Juru Ketik™ @ IT.Nusantara Group \n{datetime.now().strftime('%a, %d %b %Y %H:%M:%S.%f')[:-3]}'''.encode()
    shutil.rmtree(os.path.join(directory, 'packed/'), ignore_errors=True)
    with io.open('pack.min.template', mode='rb', ) as template:
        template = template.read().replace(b'{copyright}', copyright)
    template_size = os.path.getsize('pack.min.template')
    for dirpath, subdirs, filenames in os.walk(os.path.realpath(directory)):
        for file in [file for file in filenames if file.endswith('.js') and not file.startswith('.')]:
            input = os.path.join(dirpath, file).replace('\\', '/')
            input_size = os.path.getsize(input)
            output = os.path.join(directory, 'packed/', input.replace(directory, ''))
            if not os.path.exists(os.path.dirname(output)):
                os.makedirs(os.path.dirname(output))
            if input_size > template_size * 2:
                buffer = io.BytesIO()
                with zipfile.ZipFile(buffer, mode='a', compression=zipfile.ZIP_DEFLATED, allowZip64=False, compresslevel=compression, ) as zip:
                    zip.write(input, file)
                with open(output, mode='wb', ) as packed:
                    content = base64.b64encode(buffer.getvalue())
                    size = f'From {format(input_size)} To {format(template_size + sys.getsizeof(copyright) + sys.getsizeof(content))}'.encode()
                    packed.write(template.replace(b'{content}', content).replace(b'{size}', size))
                output_size = os.path.getsize(output)
                click.echo(f'''{click.style(f'Packed', fg='blue', bold=True)} ( {format(input_size)} ){click.style(input, fg='green', bold=True)} To ( {format(output_size)} ){click.style(output, fg='red', blink=True)}''')
                if output_size > input_size:
                    shutil.copyfile(input, output)
                    click.echo(f'''{click.style(f'Skipped', fg='blue', bold=True)} ( {format(input_size)} ){click.style(input, fg='green', bold=True)} Because Less Than ( {format(output_size)} ){click.style('Packed', fg='red', blink=True)}''')
            else:
                shutil.copyfile(input, output)
                click.echo(f'''{click.style(f'Skipped', fg='blue', bold=True)} ( {format(input_size)} ){click.style(input, fg='green', bold=True)} Because Less Than ( {format(template_size)} * 2 👉 {format(template_size * 2)} ){click.style('Template', fg='red', blink=True)}''')


if __name__ == '__main__':
    if sys.stdin and sys.stdin.isatty():
        os.system('cls' if os.name == 'nt' else 'clear')
    command()
