# sample ./setup.py file
from setuptools import setup

setup(
    name="pytest-gcov",
    version="0.0.1-alpha",
    description='Uses gcov to measure test coverage of a C library',
    license='BSD',
    author='Noufal Ibrahim',
    author_email='noufal@nibrahim.net.in' ,
    url='https://github.com/nibrahim/pytest_gcov',
    platforms=['linux'],
    install_requires = ['pytest'],
    packages = ['pytest_gcov'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Linux',
        'Topic :: Development tools',
        'Programming Language :: Python',
    ],
    # the following makes a plugin available to pytest
    entry_points = {
        'pytest11': [
            'name_of_plugin = pytest_gcov.gcov',
        ]
    },
)
