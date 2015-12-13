from setuptools import setup
import os


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
HISTORY = open(os.path.join(here, 'HISTORY.rst')).read()


version = "0.1.0.dev0"


setup(
    version=version,
    description="Plugin to integrate salt with ploy.",
    long_description=README + "\n\n" + HISTORY,
    name="ploy_salt",
    author='Florian Schulze',
    author_email='florian.schulze@gmx.net',
    license="BSD 3-Clause License",
    url='http://github.com/ployground/ploy_salt',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration'],
    include_package_data=True,
    zip_safe=False,
    packages=['ploy_salt'],
    install_requires=[
        'setuptools',
        'ploy >= 1.2.0, < 2dev',
        'salt-ssh'],
    entry_points="""
        [ploy.plugins]
        salt = ploy_salt:plugin
    """)
