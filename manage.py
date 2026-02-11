import base64
import io
import platform
import socket
from termcolor import colored
from bin import *


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
    try:
        from django.core.management import execute_from_command_line
        from django.conf import settings
    except ImportError as e:
        raise ImportError(
            '''Couldn't import Django. Are you sure it's installed and '''
            '''available on your PYTHONPATH environment variable? Did you '''
            '''forget to activate a virtual environment?'''
        ) from e
    if settings.MANAGE_CLEAR_CONSOLE and sys.stdin and sys.stdin.isatty():
        os.system('cls' if os.name == 'nt' else 'clear')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(('192.255.255.255', 1))
        ipaddress = sock.getsockname()[0]
        with io.open('core/dedication.info', mode='rb', ) as dedication:
            dedication = base64.b64decode(dedication.read())
            print(colored(dedication.decode('utf8', errors='ignore'), color='green', ))
    except:
        ipaddress = '127.0.0.1'
    finally:
        sock.close()
    os.environ.setdefault('LOCAL_ADDRESS', ipaddress)
    print('Run:', colored(' '.join(sys.argv), color='cyan', ), )
    print('Local IP Address:', colored(os.environ.get('LOCAL_ADDRESS'), color='cyan'), )
    print('Python Version:', colored(platform.python_version(), color='cyan'), )
    try:
        import django
        from django.conf import settings
        print('Django Version:', colored(django.get_version(), color='cyan'), )
        for yaml in settings.YAMLS:
            print('Yaml Loaded: ', colored(yaml, color='cyan', ), )
    except:
        pass
    print('Django Environpemt PATH:', colored(os.environ.get('PATH'), color='cyan'), )
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
