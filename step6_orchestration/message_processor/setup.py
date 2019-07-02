from setuptools import setup, find_packages
from pathlib import Path
import time

# main_module_path = Path('reddit_consumer') / 'submodule'
main_module = 'message_processor'
project_name = 'message_processor'
# namespace_packages = ['reddit_consumer']
__author__ = 'mm'
__author_email__ = 'mm'


VERSION = '0.1.0'

setup(
    name=project_name,
    author=__author__,
    author_email=__author_email__,
    python_requires='>=3.6',
    install_requires=[
        'click',
    ],
    # setup_requires=[
    #     'gitpython'
    # ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-asyncio'
    ],
    version=VERSION,
    packages=find_packages(),
    # namespace_packages=namespace_packages,
    entry_points={
        'console_scripts': [
            f'{project_name} = {main_module}.__main__:main',
        ]
    },
    # package_data={
    #     f'{main_module}': ['version.txt']
    # }
)
