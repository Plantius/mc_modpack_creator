from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='mc_modpack_creator',
    version='0.1.0',
    description='Minecraft modpack creator',
    long_description=readme,
    url='https://github.com/Plantius/mc_modpack_creator',
    packages=find_packages(exclude=('tests'))
)