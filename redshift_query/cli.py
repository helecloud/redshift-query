from . import redshift_query
import logging


def main():
    logging.basicConfig()
    redshift_query.query({})

    return 0
