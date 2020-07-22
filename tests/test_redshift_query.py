#!/usr/bin/env python

"""Tests for `redshift_query` package."""

from unittest.mock import patch, call
import unittest
import boto3
import botocore.session
import pg
from botocore.stub import Stubber
import redshift_query
import logging

logging.basicConfig()


class MockBoto(boto3.session.Session):
    def __init__(self, expected_params: dict):
        super().__init__()
        self.expected_params = expected_params

    def client(self, name: str, **kwargs):
        redshift = botocore.session.get_session().create_client('redshift', region_name='us-east-1')
        stubber = Stubber(redshift)

        stubber.add_response('get_cluster_credentials', {
            'DbUser': 'user',
            'DbPassword': 'password'
        }, self.expected_params)

        stubber.activate()

        return redshift


class TestRedshiftQuery(unittest.TestCase):
    """Tests for `redshift_query` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_query(self):
        with patch.object(pg, 'DB') as mock_method:
            mock_method().query.return_value = 'test'
            results = redshift_query.query({
                'db_name': 'name',
                'db_user': 'user',
                'cluster_host': 'host',
                'cluster_id': 'id',
                'sql_statements': 'select 1;',
                "boto_session": MockBoto(expected_params={
                    'DbUser': 'user',
                    'DbName': 'name',
                    'ClusterIdentifier': 'id',
                    'AutoCreate': False
                })
            })

        mock_method.assert_has_calls([
            call("host=host dbname=name user=user password=password port=5439 keepalives=1 "
                 "keepalives_idle=200 keepalives_interval=200 keepalives_count=6 "
                 "connect_timeout=10"),
            call().query('select 1'),
            call().close()
        ], any_order=True)

        self.assertEqual(results, ['test'])
