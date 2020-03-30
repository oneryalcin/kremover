from setuptools import setup

setup(
    name='KRemover',
    version='0.0.1',
    author='M. Oner Yalcin',
    author_email='oneryalcin@gmail.com',
    packages=['kremover'],
    entry_points = {
        'console_scripts': ['kremover-console=kremover.console:main'],
    }, 
    description='Library for removing expired Kentik client data',
    install_requires=[
        "textfsm == 1.1.0",
    ],
)
