from setuptools import setup
from os.path import join, dirname

setup(
    name='pg_stage',
    version='1.0',
    packages=['pg_stage'],
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=['Faker>=16.6.0'],
    include_package_data=True,
)
