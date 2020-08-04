from setuptools import setup

setup (
    name='snapshotalyzer-30000',
    version='0.1',
    author="Enyou Li",
    author_email="enyou_li@yahoo.com",
    description="Snapshotalyzer-30000 is a trail software for managing EC2 instances",
    license="GPLv3+",
    packages=['shotty'],
    url="https://github.com/frank-python65/snapshotalyzer-30000",
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        shotty=shotty.shotty:cli
    ''',
)
