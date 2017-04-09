from setuptools import setup

setup(
    name='gas',
    packages=['Backend'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)