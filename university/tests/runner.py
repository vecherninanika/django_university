from django.test.runner import DiscoverRunner
from django.db import connections
from types import MethodType


def setup_db(self):
    self.connect()


class PostgresRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        for conn_name in connections:
            conn = connections[conn_name]
            conn.prepare_database = MethodType(setup_db, conn)
        return super().setup_databases(**kwargs)
