# redshift-query

[![image](https://img.shields.io/pypi/v/redshift-query.svg)](https://pypi.python.org/pypi/redshift-query)
[![image](https://img.shields.io/travis/helecloud/redshift-query.svg)](https://travis-ci.com/helecloud/redshift-query)
[![image](https://readthedocs.org/projects/redshift-query/badge/?version=latest)](https://redshift-query.readthedocs.io/en/latest/?badge=latest)


## Introduction

This is a very simple library that gets credentials of a cluster via
[redshift.GetClusterCredentials](https://docs.aws.amazon.com/redshift/latest/APIReference/API_GetClusterCredentials.html)
API call and then makes a connection to the cluster and runs the provided SQL statements, once done it will close the connection and return the results.

This is useful for when you want to run queries in CLIs or based on events for example on AWS Lambdas, or on a regular
basis on AWS Glue Python Shell jobs.

## Usage

While redshift_query could be used as a library it or it's own standalone script.

It requires the following parameters supplied either as environmental variables or keys in the parameters dict passed to the function:

- DB_NAME: The database name. You can also provide this via db_name parameter to the function.
- DB_USER: The user to request credentials from. You can optionally provide this via db_user parameter to the function.
- CLUSTER_HOST: The host name of the redshift cluster. You can optionally provide this via cluster_host parameter to the function.
- CLUSTER_ID: The id of the cluster. You can optionally provide this via cluster_id parameter to the function.
- SQL_STATEMENTS: The SQL statements to run. You can optionally provide this via sql_statements parameter to the function.
This parameter is going to be formatted(via [string.format](https://docs.python.org/3/library/string.html)) with the event object that is passed to it.
This way you can have the SQL statement to be based of the event that's passed to your function, which is useful
for when you have a Lambda and it is called by an event source(S3 for example).
- REDSHIFT_QUERY_LOG_LEVEL: By default set to ERROR, which logs nothing. Normally errors are not logged and bubbled up instead so they crash the script.
If set to INFO, it will log the result of queries and if set to DEBUG it will log every thing that happens which is good for debugging why it is stuck.


### Deploying it via a glue job

You can use the [redshift-query-glue-job](https://serverlessrepo.aws.amazon.com/applications/eu-west-1/708984232979/redshift-query-glue-job) application from AWS Serverless Application Repository.

### Deploying via AWS SAM & Lambda

Here's an example that copies to a table when new manifests in S3 are written:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Resources:
  Function:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: ./redshift_query/redshift_query.py
      Handler: redshift_query.query
      Runtime: python3.8
      VpcConfig:
        SecurityGroupIds: 'sg-12312312'
        SubnetIds: 'sub-123123'
      Policies:
        - Version: '2012-10-17'
          Statement:
            - Effect: "Allow"
              Action: "redshift:GetClusterCredentials"
              Resource: "arn:aws:redshift:eu-west-1:123123123:dbuser:test/master" # https://docs.aws.amazon.com/redshift/latest/mgmt/generating-iam-credentials-role-permissions.html
      Events:
        S3:
          Type: Schedule
          Properties:
            Bucket: mybucket
            Events: s3:ObjectCreated:*
            Filter:
              S3Key:
                Rules:
                  - Name: suffix
                    Value: .manifest

      Environment:
        Variables:
          CLUSTER_ID: 'test'
          CLUSTER_HOST: 'test.j242tj1qkjuz.eu-west-1.redshift.amazonaws.com'
          DB_NAME: 'test'
          DB_USER: 'master'
          SQL_STATEMENTS: |-
            copy customer
              from {Records[0]['s3']['object']['key']}
            iam_role 'arn:aws:iam::0123456789012:role/MyRedshiftRole'
            manifest
          LOG_LEVEL: DEBUG
```

### Usage as a Library

To use the library directly you can simply provide the parameters in snake_case format:
```python
import redshift_query

results = redshift_query.query({
    'db_name': 'test',
    'db_user': 'master',
    'cluster_host': 'test.j242tj1qkjuz.eu-west-1.redshift.amazonaws.com',
    'cluster_id': 'test',
    'sql_statements': '''
        copy customer
            from 's3://mybucket/cust.manifest'
            iam_role 'arn:aws:iam::0123456789012:role/MyRedshiftRole'
            manifest;
        select * from customer;
     '''
})

[copy_results, select_results] = results

print('select results', select_results)
```

If you use redshift_query.query multiple times in your code you can use redshift_query.set_config to set the static configuration once:

```python
import redshift_query

redshift_query.set_config({
    'db_name': 'test',
    'db_user': 'master',
    'cluster_host': 'test.j242tj1qkjuz.eu-west-1.redshift.amazonaws.com',
    'cluster_id': 'test'
})

redshift_query.query({
    'sql_statements': '''
        copy customer
            from 's3://mybucket/cust.manifest'
            iam_role 'arn:aws:iam::0123456789012:role/MyRedshiftRole'
            manifest;
     '''
})
```

Optionally you can also provide boto_session, if you want to assume role or provide your own credentials:

```python
import redshift_query
import boto3

redshift_query.query({
    'boto_session': boto3.session.Session(profile_name='production'),
    'sql_statements': 'select 1;'
})
```

### As a CLI

```
$ DB_USER=neshat DB_NAME=test CLUSTER_ID=test CLUSTER_HOST=test.3j232jjqji21.eu-west-1.redshift.amazonaws.com SQL_STATEMENTS='select 1;' REDSHIFT_QUERY_LOG_LEVEL=DEBUG redshift_query
DEBUG:redshift_query:Passed Event: {}
DEBUG:redshift_query:Passed this_config with added defaults: {'db_name': 'test', 'db_user': 'neshat', 'cluster_host': 'test.3j232jjqji21.eu-west-1.redshift.amazonaws.com', 'cluster_id': 'test', 'sql_statements': 'select 1;', 'boto_session': None}
DEBUG:redshift_query:Received Credentials
DEBUG:redshift_query:Connected
DEBUG:redshift_query:Running select 1
INFO:redshift_query:Statement "?column?
--------
       1
(1 row)" result:
```

Credits
-------

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
