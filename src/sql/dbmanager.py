from configparser import ConfigParser

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DBManager:

    def __init__(self):
        self.create_db()
        conn = self.connect(self.load_config())

        with conn:
            with conn.cursor() as cur:
                cur.execute(self.get_command_sql_init())

    def load_config_without_db(self, filename='database.ini', section='postgresql_empty') -> dict:
        return self.load_config(filename, section)

    def load_config(self, filename='database.ini', section='postgresql') -> dict:
        parser = ConfigParser()
        parser.read(filename)

        # get section, default to postgresql
        config = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                config[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return config

    def connect(self, config):
        """ Connect to the PostgreSQL database server """
        try:
            # connecting to the PostgreSQL server
            with psycopg2.connect(**config) as conn:
                print('Connected to the PostgreSQL server.')
                return conn
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)

    def get_command_db_create(self) -> str:
        return self.get_sql_cmd("db_create.sql")

    def get_command_sql_init(self) -> str:
        return self.get_sql_cmd("db_create_tables.sql")

    def get_sql_cmd(self, filepath: str) -> str:
        return open(filepath, "r", encoding="utf-8").read()

    def create_db(self) -> bool:
        # Из-за особенностей обратки команды CREATE DATABASE
        # нужно по особенному подключаться к СУБД
        # и обязательно БЕЗ контекстного менеджера
        operation_result = True
        config = self.load_config_without_db()
        conn = self.connect(config)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cur = conn.cursor()
        try:
            cmd = self.get_command_db_create()
            cur.execute(cmd)
            # cur.execute("CREATE DATABASE IF NOT EXISTS hh_vac")
            # cur.execute(
            #     """SELECT 'CREATE DATABASE hh_vac'
            #     WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'hh_vac')""")
        except Exception as e:
            print(e)
            operation_result = False

        conn.close()
        return operation_result

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        pass

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        pass

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        pass

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass

    def get_vacancies_with_keyword(self):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        pass
