from setuptools import setup
from os.path import join, dirname

setup(
    name='pg_stage',
    version='0.3.1',
    packages=['pg_stage'],
    package_dir={'': 'src'},
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=['typing-extensions>=4.5.0', 'mimesis==4.1.3'],
    extras_require={'dev': ['pytest']},
    include_package_data=True,
)
