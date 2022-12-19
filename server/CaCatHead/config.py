from pathlib import Path

from dotenv import load_dotenv
from pyaml_env import parse_config, BaseConfig

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

config_path = BASE_DIR / 'cacathead.yml'
if not config_path.is_file():
    config_path = BASE_DIR / 'cacathead.yaml'
if not config_path.is_file():
    config_path = BASE_DIR / 'cacathead.example.yml'

cacathead_config = BaseConfig(parse_config(str(config_path)))
