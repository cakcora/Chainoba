from setuptools import setup

# TODO
# Update the setup part

with open("requirements.txt", 'r') as fp:
    packages = [line.rstrip('\n') for line in fp.readlines()]

setup(
    name='COMP 7570/4060',
    version='1.0',
    description='Blockchain Analytics',
    packages=['COMP 7570/4060'],  # same as name
    install_requires=packages
)
