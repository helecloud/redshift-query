import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="redshift-query", # Replace with your own username
    version="0.0.3",
    author="Farid Nouri Neshat",
    author_email="faridn@helecloud.com",
    description="A simple library that runs queries on redshift!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/helecloud/redshift_query",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pygresql~=5.2',
        'boto3~=1.13.6'
    ]
)
