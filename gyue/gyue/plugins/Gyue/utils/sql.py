import sqlite3
import gyue.gyue.plugins.Gyue.GlobalScope as gs
class SQLiteHelper:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def ccreateTable(self, table_name, columns:dict):
        columns_str = ', '.join([f"{name} {datatype}" for name, datatype in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
        return self.cexecute(query)

    def createTable(self, table_name, columns: dict):
        columns_str = ', '.join([f"{name} {datatype}" for name, datatype in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
        return self.execute(query)
    def cexecute(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            if query.strip().upper().startswith("SELECT"):
                result = self.cursor.fetchall()
                columns = [desc[0] for desc in self.cursor.description]
                result_dict = [dict(zip(columns, row)) for row in result]
                return result_dict
            else:
                self.conn.commit()
                return True
        except sqlite3.Error as e:
            print("Error executing query:", e)
            return None
        finally:
            self.close()
    def execute(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            if query.strip().upper().startswith("SELECT"):
                result = self.cursor.fetchall()
                columns = [desc[0] for desc in self.cursor.description]
                result_dict = [dict(zip(columns, row)) for row in result]
                return result_dict
            else:
                self.conn.commit()
                return True
        except sqlite3.Error as e:
            print("Error executing query:", e)
            return None
        finally:
            pass

    def cinsert(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return self.cexecute(query, tuple(data.values()))

    def cupdate(self, table, data, condition):
        set_values = ', '.join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE {table} SET {set_values} WHERE {condition}"
        return self.cexecute(query, tuple(data.values()))

    def cdelete(self, table, condition):
        query = f"DELETE FROM {table} WHERE {condition}"
        return self.cexecute(query)

    def cselect(self, table, columns='*', condition=None):
        query = f"SELECT {columns} FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        return self.cexecute(query)
    def insert(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return self.execute(query, tuple(data.values()))

    def update(self, table, data, condition):
        set_values = ', '.join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE {table} SET {set_values} WHERE {condition}"
        return self.execute(query, tuple(data.values()))

    def delete(self, table, condition):
        query = f"DELETE FROM {table} WHERE {condition}"
        return self.execute(query)

    def select(self, table, columns='*', condition=None):
        query = f"SELECT {columns} FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        return self.execute(query)

    def close(self):
        if self.conn is not None:
            self.conn.close()

# Example Usage:
# helper = SQLiteHelper("example.db")
# helper.insert("table_name", {"column1": "value1", "column2": "value2"})
# helper.update("table_name", {"column1": "new_value"}, "column2 = 'value2'")
# helper.delete("table_name", "column1 = 'value1'")
# result = helper.select("table_name", "*", "column2 = 'new_value'")
# print(result)

