import typing
import datetime
import logging
import sqlite3


class Database():
    def __init__(self, namebase: str):
        """Connect data base
        
        Args:
            namebase (str): write name for database
                ex: "profile"
        """
        self.namebase = namebase
        self.base = sqlite3.connect(f'{namebase}.db')
        self.cursor = self.base.cursor()

        if self.base:
            logging.info("Database connected!")
        else:
            logging.info(self.base)


class TableUser(Database):
    def __init__(self, namebase: str, name_table: str):
        super().__init__(namebase)

        self.name_table_user = name_table

        tabel = f'''CREATE TABLE IF NOT EXISTS {self.name_table_user}(
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            spred_percent TEXT,
            payment_methods TEXT,
            deposit TEXT,
            fiat TEXT,
            asset TEXT,
            subscribe INTEGER)'''

        self.cursor.execute(tabel)
        self.base.commit()

    def create_user(self, user_id: int, username: str):
        user = self.cursor.execute(f'SELECT 1 FROM {self.name_table_user} WHERE user_id == {user_id}').fetchone()
        if not user:
            self.cursor.execute(f'INSERT INTO {self.name_table_user} VALUES(?, ?, ?, ?, ?, ?, ?, ?)',
                                (user_id, username, "0", "RosBankNew", "0", "RUB", "empty", 0))
            self.base.commit()

    def check_parameters(self, user_id: int, parameters: str) -> bool:
        parameters = str(self.cursor.execute(
            f'SELECT {parameters} FROM {self.name_table_user} WHERE user_id == {user_id}').fetchone())

        if parameters == "empty":
            return False
        else:
            return True

    def value_parameters(self, user_id: int, parameter: str) -> str:
        validation = self.check_parameters(user_id, parameter)
        if not validation:
            raise ValueError("Parameter is empty!")

        value = str(self.cursor.execute(
            f'SELECT {parameter} FROM {self.name_table_user} WHERE user_id == {user_id}').fetchone()[0])

        return value

    def parameter_replace(self, user_id: int, parameter: str, new_parameter_value: str) -> str:
        userdata = self.cursor.execute(f'SELECT 1 FROM {self.name_table_user} WHERE user_id = {user_id}').fetchone()
        if not userdata:
            return "Ошибка получения userdata из parameter_replace"
        validation = self.check_parameters(user_id, parameter)
        if not validation:
            raise ValueError("Parameter is empty!")

        self.cursor.execute(f"UPDATE {self.name_table_user} SET {parameter} = ? WHERE user_id = {user_id}",
                            (new_parameter_value,))

        self.cursor.execute(
            f'SELECT {parameter} FROM {self.name_table_user} WHERE user_id == {user_id}')
        result = self.cursor.fetchone()
        self.base.commit()
        return result

    def check_subscription(self, user_id: int) -> bool:
        self.cursor.execute(f'SELECT subscribe FROM {self.name_table_user} WHERE user_id = ?', (user_id,))
        result = self.cursor.fetchone()

        if result:
            return bool(result[0])

        return False


class NotificationDatabase(TableUser):
    def __init__(self, name_table: str):
        self.name_table_notifi = name_table

        tabel = f'''CREATE TABLE IF NOT EXISTS {self.name_table_notifi}(
            user_id INTEGER PRIMARY KEY,
            notification_time INTEGER,
             TEXT)'''

        self.cursor.execute(tabel)
        self.base.commit()

    def create_notification(self, user_id: int) -> None:
        user = self.cursor.execute(f'SELECT 1 FROM {self.name_table_notifi} WHERE user_id == {user_id}').fetchone()
        if not user:
            self.cursor.execute(f'INSERT INTO {self.name_table_notifi} VALUES(?, ?,)',
                                (user_id, 0))
            self.base.commit()

    def get_notifacation_time(self, user_id: int) -> int:
        text_execute = f'SELECT notification_time FROM {self.name_table_notifi} WHERE user_id == {user_id}'
        return int(self.cursor.execute(text_execute).fetchone())

    def set_notifacation_time(self, user_id: int, time: int) -> None:
        text_execute = f'UPDATE {self.name_table_notifi} SET notification_time = ? WHERE user_id == {user_id}'
        self.cursor.execute(text_execute, str(time))


if __name__ == "__main__":
    pass
