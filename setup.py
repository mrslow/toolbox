from setuptools import setup

setup(
    name='toolbox',
    version='0.5.1',
    description='Toolbox for server applications',
    install_requires=['aiohttp', 'asyncpg', 'pyyaml'],
    packages=['toolbox']
)
