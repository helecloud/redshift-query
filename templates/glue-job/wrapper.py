import sys
import os
from awsglue.utils import getResolvedOptions
import redshift_query
import logging

args = getResolvedOptions(sys.argv,
                          ['db_name',
                           'db_user',
                           'cluster_id',
                           'cluster_host',
                           'sql_statements',
                           'log_level'])

logging.basicConfig(level=args['log_level'], stream=sys.stdout)
logging.getLogger('redshift_query').setLevel(args['log_level'])

redshift_query.query(args)
