from setuptools import setup

setup(
    name='app',
    packages=['Backend'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)