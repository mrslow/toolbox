from setuptools import setup

setup(
    name='toolbox',
    version='0.4.0',
    description='Toolbox for server applications',
    install_requires=['aiohttp', 'acyncpg'],
    packages=['toolbox']
)
