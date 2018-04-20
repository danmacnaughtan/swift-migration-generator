"""setup.py
"""
from setuptools import setup, find_packages

setup(
    name='swift_migration_generator',
    version='1.0',
    description='Generate merge files for the SQLiteMigrationManager.swift framework.',
    scripts=['swift_migration_generator.py'],
    install_requires=['Click>=6.0'],
    entry_points={'console_scripts': ['swift_migration_generator=swift_migration_generator:main']}
)

