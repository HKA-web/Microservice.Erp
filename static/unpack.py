import base64
import io
import os
import os.path
import shutil
import sys
import zipfile

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
    '''JavaScript Unpacker For Unpack From Packer, By ©Tukang Pecut Juru Ketik™ @ IT.Nusantara Group'''
    directory = directory.replace('\\', '/')
    directory = f'{directory}/' if not directory.endswith('/') else directory
    shutil.rmtree(os.path.join(directory, 'unpacked/'), ignore_errors=True)
    template_size = os.path.getsize('pack.min.template')
    for dirpath, subdirs, filenames in os.walk(os.path.realpath(directory)):
        for file in [file for file in filenames if file.endswith('.js') and not file.startswith('.')]:
            input = os.path.join(dirpath, file).replace('\\', '/')
            input_size = os.path.getsize(input)
            output = os.path.join(directory, 'unpacked/', input.replace(directory, ''))
            if not os.path.exists(os.path.dirname(output)):
                os.makedirs(os.path.dirname(output))
            if input_size > template_size * 2:
                with open(input, mode='rb') as packed:
                    zipped = []
                    for chunk in packed:
                        if chunk.startswith(b'var base64zip = '):
                            zipped = base64.decodebytes(chunk.replace(b'var base64zip = "', b'').replace(b'";', b''))
                            break
                    if zipped is not None and len(zipped) > 0:
                        buffer = io.BytesIO(zipped)
                        with zipfile.ZipFile(buffer, mode='a', compression=zipfile.ZIP_DEFLATED, allowZip64=False, compresslevel=compression, ) as zip:
                            zip.extract(file, os.path.dirname(output))
                            output_size = os.path.getsize(output)
                            click.echo(f'''{click.style(f'Unpacked', fg='blue', bold=True)} ( {format(input_size)} ){click.style(input, fg='green', bold=True)} To ( {format(output_size)} ){click.style(output, fg='red', blink=True)}''')
                    else:
                        shutil.copyfile(input, output)
                        output_size = os.path.getsize(output)
                        click.echo(f'''{click.style(f'Skipped', fg='blue', bold=True)} ( {format(input_size)} ){click.style(input, fg='green', bold=True)} Because ( {format(output_size)} ){click.style('Not Packed', fg='red', blink=True)}''')
            else:
                shutil.copyfile(input, output)
                click.echo(f'''{click.style(f'Skipped', fg='blue', bold=True)} ( {format(input_size)} ){click.style(input, fg='green', bold=True)} Because Less Than ( {format(template_size)} * 2 👉 {format(template_size * 2)} ){click.style('Template', fg='red', blink=True)}''')


if __name__ == '__main__':
    if sys.stdin and sys.stdin.isatty():
        os.system('cls' if os.name == 'nt' else 'clear')
    command()
