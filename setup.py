from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='pg_stage',
    version='0.1.5',
    packages=['pg_stage'],
    package_dir={'': 'src'},
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=['Faker>=16.6.0'],
    extras_require={'dev': ['pytest']},
    include_package_data=True,
)
