# MIT License
#
# Copyright (c) 2020 Helecloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pg
import boto3
import os
import logging

config = {
    'db_name': os.getenv('DB_NAME') or None,
    'db_user': os.getenv('DB_USER'),
    'cluster_host': os.getenv('CLUSTER_HOST'),
    'cluster_id': os.getenv('CLUSTER_ID'),
    'sql_statements': os.getenv('SQL_STATEMENTS'),
    'boto_session': None
}

logger = logging.getLogger('redshift_query')
logger.setLevel(os.getenv('REDSHIFT_QUERY_LOG_LEVEL', 'ERROR'))


def set_config(new_config):
    global config
    config = {**config, **new_config}


def query(event, context=None):
    logger.debug('Passed Event: %s', event)

    this_config = {**config, **event}

    session = this_config['boto_session'] or boto3.session.Session()

    if not isinstance(session, boto3.session.Session):
        raise RuntimeError('Not a valid boto3 session. Please check your configuration')

    client = session.client('redshift')

    logger.debug('Passed this_config with added defaults: %s', this_config)

    credentials = client.get_cluster_credentials(
        DbUser=this_config['db_user'],
        DbName=this_config['db_name'],
        ClusterIdentifier=this_config['cluster_id'],
        AutoCreate=False,
    )

    logger.debug('Received Credentials')

    db = pg.DB(f"host={this_config['cluster_host']} "
               f"dbname={this_config['db_name']} "
               f"user={credentials['DbUser']} "
               f"password={credentials['DbPassword']} "
               'port=5439 '
               'keepalives=1 keepalives_idle=200 keepalives_interval=200 keepalives_count=6 '
               'connect_timeout=10')

    logger.debug('Connected')

    statements = this_config['sql_statements'].format(**event).strip().split(';')

    def run(statement):
        logger.debug('Running %s', statement)
        result = db.query(statement)
        logger.info('Statement "%s" result:', result)
        return result

    results = [
        run(statement)
        for statement in statements
        if statement
    ]

    db.close()

    return results
