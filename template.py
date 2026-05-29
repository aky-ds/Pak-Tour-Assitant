import os

from pathlib import Path

list_of_files = [
    '.github/workflows/.gitkeep',
    'src/__init__.py',
    "src/components/__init__.py",
    "src/components/graph.py",
    "src/components/states.py",
    "src/components/nodes.py",
    "src/components/Mtools.py",
    "src/logger/__init__.py",
    "src/logger/logger.py",
    "src/exceptions/__init__.py",
    "src/exception.py",
    "tests/unit/__init__.py",
    "tests/integration/__init__.py",
    "tox.ini",
    'requirements.txt',
    "requirements_dev.txt",
    "setup.py",
    "init_setup.sh",
    "setup.cfg",
    "pyproject.toml",
    "app.py",
    "experiments/experiments.ipynb",
    "Docker"
]


for file in list_of_files:
    file_path=Path(file)
    file_dir,file_name=os.path.split(file_path)
    if file_dir !="":
        os.makedirs(file_dir, exist_ok=True)
    
    if not os.path.exists(file_path):
        with open(file_path,'w') as f:
            pass
        