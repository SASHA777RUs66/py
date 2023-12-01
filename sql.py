import sqlite3

from help_functions import check_choice

class Database:
    def __init__(self, db_file):
        self.connect = sqlite3.connect("carsRepairing.sql")
        self.cursor = self.connect.cursor()

    def query_for_db(self, query, values=None):
        with self.connect:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)

    def create_table(self, sender, columns):
        db_name = sender.__class__.__name__
        allColumns = ", ".join(f"{name} {type}" for name, type in columns.items())
        query = F"""
        CREATE TABLE IF NOT EXISTS {db_name} (
        {allColumns}
        );"""
        self.query_for_db(query)

    def update_table(self, sender, columns, params=dict()):
        db_name = sender.__class__.__name__
        column = " and ".join(f"{column} = ?" for column in columns.keys())
        parameters = " and ".join(f"{param} = ?" for param in params.keys())
        query = F"""
        UPDATE {db_name} SET {column} WHERE {parameters}"""
        args = list()
        for arg in columns.keys():
            args.append(columns[arg])
        for arg in params.keys():
            args.append(params[arg])
        self.query_for_db(query, args)

    def select_from(self, sender, columns, params=dict()):
        db_name = sender.__class__.__name__
        column = ", ".join(f"{col}" for col in columns)
        parameters = " and ".join(f"{param} = ?" for param in params.keys())
        values = list(params.values()) if parameters else list()
        query = F"""
        SELECT {column} FROM {db_name} {f"where {parameters}"if parameters else ""};"""
        with self.connect:
            return self.cursor.execute(query, values).fetchall()

    def insert_into(self, sender, columns):
        db_name = sender.__class__.__name__
        column = ", ".join(f"{col}" for col in columns)
        values = list()
        for arg in columns.keys():
            values.append(columns[arg])
        query = f"""
        INSERT INTO {db_name} ({column}) VALUES ({", ".join("?" for _ in columns.keys())})"""
        self.query_for_db(query, values)

    def delete_from(self, sender, params):
        db_name = sender.__class__.__name__
        parameters = " and ".join(f"{param} = ?" for param in params.keys())
        values = list(params.values()) if parameters else list()
        query = f"""
        DELETE FROM {db_name} WHERE {parameters}"""
        self.query_for_db(query, values)

class Users_db(Database):
    def __init__(self, db_file):
        super().__init__(db_file)
        self.__name = ""
        self.__role = ""
        self.__password = ""

    def check_name(self):
        names = self.select_from(self, ["user_name"])
        all_names = list()
        for item in names:
            all_names.append("".join(list(item)))
        self.__name = check_choice(str, "Введите Ваше имя: ")
        while self.__name in all_names:
            self.__name = check_choice(str, "Это имя занято(\nВведите Ваше имя: ")

    def set_name(self, name):
        self.__name = name

    def set_role(self, role):
        self.__role = role

    def set_pass(self, password):
        self.__password = password

    @property
    def name(self):
        return self.__name

    @property
    def role(self):
        return self.__role

    @property
    def password(self):
        return self.__password

class Workers_db(Database):
    def __init__(self, db_file):
        super().__init__(db_file)
        self.__name = ""
        self.__code = ""

    def set_name(self, name):
        self.__name = name

    def set_code(self, code):
        self.__code = code

    @property
    def code(self):
        return self.__code

    @property
    def name(self):
        return self.__name

    def update_table(self, job="", **kwargs):
        return super().update_table(self, {"worker_prof": job}, {'worker_code': self.__code})



class Cars_db(Database):
    def __init__(self, db_file):
        super().__init__(db_file)
        self.__model = ""
        self.__number = ""

    def set_car(self):
        self.__model = check_choice(str, "Введите модель машины: ")
        self.__number = check_choice(str, "Введите номер машины: ")

    @property
    def model(self):
        return self.__model

    @property
    def number(self):
        return self.__number


class Orders_db(Database):
    def __init__(self, db_file):
        super().__init__(db_file)


class Customers_db(Database):
    def __init__(self, db_file):
        super().__init__(db_file)

    def select_from(self, **kwargs):
        return super().select_from(self, ['customer_title', 'customer_address'])






