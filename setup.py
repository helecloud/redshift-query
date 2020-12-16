#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'pygresql~=5.2',
    'boto3~=1.16.37'
]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Farid Nouri Neshat",
    author_email='faridn@helecloud.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A simple library that runs queries on redshift!",
    entry_points={
        'console_scripts': [
            'redshift_query=redshift_query.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='redshift query sql serverless lambda glue aws',
    name='redshift-query',
    packages=find_packages(include=['redshift_query', 'redshift_query.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/helecloud/redshift-query',
    version='0.1.4',
    zip_safe=False,
)
