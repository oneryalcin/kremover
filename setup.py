from setuptools import setup

setup(
    name='KRemover',
    version='0.0.1',
    author='M. Oner Yalcin',
    author_email='oneryalcin@gmail.com',
    packages=['kremover'],
    # scripts=['bin/script1', 'bin/script2'],
    # url='http://pypi.python.org/pypi/PackageName/',
    # license='LICENSE.txt',
    description='Library for removing exired Kentik client data',
    # long_description=open('README.txt').read(),
    install_requires=[
        "textfsm == 1.1.0",
    ],
)
