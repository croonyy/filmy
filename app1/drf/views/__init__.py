from importlib import import_module
import os
from filmy.settings import BASE_DIR

# views_path = os.path.join(BASE_DIR, 'app1', 'drf', 'views')
rel_path = os.path.relpath(os.path.dirname(__file__), BASE_DIR).split('\\')

for file in os.listdir(os.path.dirname(__file__)):
    # if file in ['__init__.py', '__pycache__']:
    #     continue

    file_name, ext = os.path.splitext(file)
    if ext == '.py' and file_name != '__init__':
        import_module("app1.drf.views." + file_name)

