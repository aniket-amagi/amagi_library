#!/usr/bin/python3
# coding= utf-8
"""
This scripts has method which help to access Dynamo DB
Xref : https://martinapugliese.github.io/interacting-with-a-dynamodb-via-boto3/
"""
import logging

from boto3.dynamodb.conditions import Key

from amagi_library.boto3_helper.resource import Resource


class DynamoAccessor(object):
    """
        This Class handles access of dynamo DB resource
    """

    def __init__(self, **kwargs):
        self.aws_details = None
        self.__dict__.update(kwargs)

        self.dynamo_db_resource = Resource(aws_details=self.aws_details).return_resource(service_name='dynamodb')

        logging.debug("Instance variables for DynamoResource : " + str(self.__dict__))

    def get_table_metadata(self, table_name):
        """
        Get some metadata about chosen table.
        """
        table = self.dynamo_db_resource.Table(table_name)

        logging.debug("Response from get_table_metadata : " + str(table))

        return {
            'num_items': table.item_count,
            'primary_key_name': table.key_schema[0],
            'status': table.table_status,
            'bytes_size': table.table_size_bytes,
            'global_secondary_indices': table.global_secondary_indexes
        }

    def read_table_item(self, table_name, pk_name, pk_value):
        """
        Return item read by primary key.
        """
        logging.debug(f"Read table {table_name} with PK name : {pk_name} and PK value : {pk_value}")

        table = self.dynamo_db_resource.Table(table_name)

        response = table.get_item(Key={pk_name: pk_value})
        logging.debug(f"Response from Dynamo DB : {response}")

        return response

    def add_item(self, table_name, col_dict):
        """
        Add one item (row) to table. col_dict is a dictionary {col_name: value}.
        """
        logging.debug(f"Item added to table {table_name} : {col_dict}")

        table = self.dynamo_db_resource.Table(table_name)

        response = table.put_item(Item=col_dict)
        logging.debug(f"Response from Dynamo DB : {response}")

        return response

    def delete_item(self, table_name, pk_name, pk_value):
        """
        Delete an item (row) in table from its primary key.
        """
        table = self.dynamo_db_resource.Table(table_name)

        response = table.delete_item(Key={pk_name: pk_value})
        logging.debug(f"Response from Dynamo DB : {response}")

        return response

    def scan_table(self, table_name, filter_key=None, filter_value=None):
        """
        Perform a scan operation on table.
        Can specify filter_key (col name) and its value to be filtered.
        """
        table = self.dynamo_db_resource.Table(table_name)

        if filter_key and filter_value:
            filtering_exp = Key(filter_key).eq(filter_value)
            response = table.scan(FilterExpression=filtering_exp)
        else:
            response = table.scan()

        logging.debug(f"Response from Dynamo DB : {response}")
        return response

    def query_table(self, table_name, filter_key=None, filter_value=None):
        """
        Perform a query operation on the table.
        Can specify filter_key (col name) and its value to be filtered.
        """
        table = self.dynamo_db_resource.Table(table_name)

        if filter_key and filter_value:
            filtering_exp = Key(filter_key).eq(filter_value)
            response = table.query(KeyConditionExpression=filtering_exp)
        else:
            response = table.query()

        logging.debug(f"Response from Dynamo DB : {response}")
        return response

    def scan_table_allpages(self, table_name, filter_key=None, filter_value=None):
        """
        Perform a scan operation on table.
        Can specify filter_key (col name) and its value to be filtered.
        This gets all pages of results. Returns list of items.
        """
        table = self.dynamo_db_resource.Table(table_name)

        if filter_key and filter_value:
            filtering_exp = Key(filter_key).eq(filter_value)
            response = table.scan(FilterExpression=filtering_exp)
        else:
            response = table.scan()

        items = response['Items']
        while True:
            if response.get('LastEvaluatedKey'):
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                items += response['Items']
            else:
                break

        logging.debug(f"Response from Dynamo DB : {items}")
        return items


if __name__ == "__main__":
    # LOGGING #
    logging_format = "%(asctime)s::%(funcName)s::%(levelname)s:: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%Y/%m/%d:%H:%M:%S:%Z:%z")
    logger = logging.getLogger(__name__)
