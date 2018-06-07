from setuptools import setup

setup(
    name='snapshotalyzer69',
    version='0.1',
    author='Jeff',
    author_email="jeff@gmail.com",
    description='Snapshot management tool for AWS',
    license='GPLv3+',
    packages=['snappy'],
    url="https://github.com/spotstory/snapshotalyzer69",
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        snappy=snappy.snappy:cli
    ''',
)
