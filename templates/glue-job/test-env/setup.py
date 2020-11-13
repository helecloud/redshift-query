import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="test_env",
    version="0.0.1",

    description="Creates a Redshift cluster and tests redshift query glue job stack",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "test_env"},
    packages=setuptools.find_packages(where="test_env"),

    install_requires=[
        "aws-cdk.core==1.52.0",
        'aws-cdk.aws-ec2==1.52.0',
        'aws-cdk.aws-redshift==1.52.0',
        'aws-cdk.aws-sam==1.52.0'
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
