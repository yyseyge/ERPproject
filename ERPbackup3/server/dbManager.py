import threading
import traceback

import pymysql

lock = threading.Lock()

class DBManager:
    _instance = None
    _connection = None
    _cursor = None

    def __new__(cls, host, user, password, port, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                charset="utf8mb4",
                database="erp_db",
                port=port)
            cls._cursor = cls._connection.cursor()
        return cls._instance

    def __del__(self):
        self.close()

    def close(self):
        if self._cursor:
            self._cursor.close()
        if self._connection:
            self._connection.close()
            self._cursor = None
            self._connection = None

    def query(self, query, params=None):
        try:
            lock.acquire()
            print('query:',query)
            print('params:',params)
            self._cursor.execute(query, params)
            self._connection.commit()
            result = self._cursor.fetchall()
            print('result:',result)
            lock.release()
            return result
        except Exception as e:
            print(traceback.format_exc())
            print(f"Query failed. Error: {e}")
            lock.release()
            return None

    def transaction(self, queries):
        try:
            lock.acquire()
            self._connection.autocommit(False)
            for query, params in queries:
                print('query:', query)
                print('params:', params)
                self._cursor.execute(query, params)
            self._connection.commit()
            lock.release()
            return True
        except Exception as e:
            self._connection.rollback()
            print(f"Transaction failed. Error: {e}")
            lock.release()
            return False