from os.path import dirname, join

from setuptools import setup

setup(
    name='pg_stage',
    version='0.4.0',
    packages=['pg_stage'],
    package_dir={'': 'src'},
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=['typing-extensions>=4.5.0', 'mimesis==4.1.3'],
    extras_require={'dev': ['pytest']},
    include_package_data=True,
    license_files=('LICENSE.txt',),
)
