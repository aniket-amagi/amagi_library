from abc import abstractmethod


class StatusManager(object):

    @abstractmethod
    def publish_status(self, state, asset_id, **kwargs):
        pass

    @abstractmethod
    def get_last_status(self, asset_id):
        pass

    @abstractmethod
    def get_status(self, **kwargs):
        pass

    @classmethod
    def get_status_manager(cls, typ, **kwargs):
        if typ == "chicane":
            from amagi_library.status_manager.chicane.chicane import Chicane
            return Chicane(**kwargs)
        elif typ == "dynamodb":
            from amagi_library.status_manager.dynamodb.dynamodb import DynamoDB
            return DynamoDB(**kwargs)
