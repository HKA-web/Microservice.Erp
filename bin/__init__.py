import os
import sys
from pathlib import Path

cwd = Path(__file__).resolve().parent
# executable library here :
sys.path.append(os.path.abspath(os.path.join(cwd, 'gettext/bin')))
sys.path.append(os.path.abspath(os.path.join(cwd, 'redis')))
sys.path.append(os.path.abspath(os.path.join(cwd, 'ffmpeg/bin')))
sys.path.append(os.path.abspath(os.path.join(cwd, 'wkhtmltopdf/bin')))
sys.path.append(os.path.abspath(os.path.join(cwd, 'nodejs')))
sys.path.append(os.path.abspath(os.path.join(cwd, 'git/bin')))
sys.path.append(os.path.abspath(os.path.join(cwd, 'cargo/bin')))
sys.path.append(os.path.abspath(os.path.join(cwd, 'erlang/bin')))
sys.path.append(os.path.abspath(os.path.join(cwd, 'rabbitmq/bin')))
sys.path.append(os.path.abspath(os.path.join(cwd, 'nginx')))
sys.path.append(os.path.abspath(os.path.join(cwd, 'zip')))
# add sys.path to environment
os.environ['PATH'] += os.pathsep + os.pathsep.join(sys.path)
