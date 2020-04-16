#!/usr/bin/python3
# coding= utf-8
"""
This scripts creates boto3 session based Assumed Role Credentials
"""
import datetime
import logging

import boto3
import botocore
from dateutil.tz import tzlocal


def assumed_role_session(role_arn, base_session):
    """
    This method is ripped of from below url to get AWS session using AssumeRoleProvider
    xref: https://stackoverflow.com/questions/44171849/aws-boto3-assumerole-example-which-includes-role-usage\
    :param role_arn: URI for role, example : "'arn:aws:iam::123456789:role/role-crossaccount-xyz"
    :param base_session: Base Session for which ARP has been provided
    :return: Boto3 session with ARP
    """
    fetcher = botocore.credentials.AssumeRoleCredentialFetcher(
        client_creator=base_session.create_client,
        source_credentials=base_session.get_credentials(),
        role_arn=role_arn
    )
    creds = botocore.credentials.DeferredRefreshableCredentials(
        method='assume-role',
        refresh_using=fetcher.fetch_credentials,
        time_fetcher=lambda: datetime.datetime.now(tzlocal())
    )
    botocore_session = botocore.session.Session()
    botocore_session._credentials = creds
    return boto3.Session(botocore_session=botocore_session)


if __name__ == "__main__":
    # LOGGING #
    logging_format = "%(asctime)s::%(funcName)s::%(levelname)s:: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%Y/%m/%d:%H:%M:%S:%Z:%z")
    logger = logging.getLogger(__name__)
