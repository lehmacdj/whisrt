from setuptools import setup

setup(
    entry_points={
        'console_scripts': [
            'whisrt = whisrt.main:main',
        ],
    },
)
