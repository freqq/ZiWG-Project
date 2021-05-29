"""
ZiWG Text Analysis
"""

from setuptools import setup, find_packages

REQUIREMENTS = [
    'pandas',
    'pymarc',
]

setup(
    name='ziwg-analysis',
    version='0.0.1',
    author='PWr',
    description='ZiWG Analysis',
    package_dir={'': 'tools'},
    packages=find_packages('tools'),
    include_package_data=True,
    install_requires=REQUIREMENTS
)
