import os
from configparser import ConfigParser

import psycopg2
import psycopg2.errors
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DBManager:

    def __init__(self):
        self.__conn = None

    def __del__(self):
        print("!!! Connection close!")
        if self.__conn is not None:
            self.__conn.commit()
            self.__conn.close()

    def load_config_without_db(self, filename='database.ini', section='postgresql_empty') -> dict:
        return self.load_config(filename, section)

    def load_config(self, filename='database.ini', section='postgresql') -> dict:
        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        abs_file_path = os.path.join(script_dir, filename)

        parser = ConfigParser()
        parser.read(abs_file_path)

        # get section, default to postgresql
        config = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                config[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, abs_file_path))

        return config

    def connect(self, config):
        """ Connect to the PostgreSQL database server """
        try:
            # connecting to the PostgreSQL server
            self.__conn = psycopg2.connect(**config)
            print('!!! Connected to the PostgreSQL server.')
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)

    def init_tables(self):
        with self.__conn.cursor() as cur:
            cur.execute(self.get_command_sql_is_tables_exists())
            if not int(cur.fetchone()[0]):
                cur.execute(self.get_command_sql_init())

        print("!!! Init complete")

    def insert_employers(self, employers: list[tuple]):
        with self.__conn.cursor() as cur:
            for emp_info in employers:
                cur.execute(self.get_command_sql_insert_into_employers(), emp_info)

        print("!!! Employers inserted (updated)")

    def insert_vacancies_and_salaries(self, vacancies_and_salaries: list[tuple]):
        with self.__conn.cursor() as cur:
            for vac_info in vacancies_and_salaries:
                cur.execute(self.get_command_db_insert_into_vacancies(), vac_info[0])
                cur.execute(self.get_command_db_insert_into_salaries(), vac_info[1])

        print("!!! Vacancies and salaries inserted (updated)")

    def get_command_db_create(self) -> str:
        return self.get_sql_cmd("db_create.sql")

    def get_command_sql_init(self) -> str:
        return self.get_sql_cmd("db_create_tables.sql")

    def get_command_sql_is_tables_exists(self) -> str:
        return self.get_sql_cmd("db_is_tables_exists.sql")

    def get_command_sql_insert_into_employers(self) -> str:
        return self.get_sql_cmd("db_insert_into_employers.sql")

    def get_command_db_insert_into_vacancies(self) -> str:
        return self.get_sql_cmd("db_insert_into_vacancies.sql")

    def get_command_db_insert_into_salaries(self) -> str:
        return self.get_sql_cmd("db_insert_into_salaries.sql")

    def get_command_db_select_all_vacancies(self) -> str:
        return self.get_sql_cmd("db_select_all_vacancies.sql")

    def get_command_db_select_avg_salary(self) -> str:
        return self.get_sql_cmd("db_select_avg_salary.sql")

    def get_command_db_select_companies_and_vacancies(self) -> str:
        return self.get_sql_cmd("db_select_companies_and_vacancies.sql")

    def get_command_db_select_vacancies_with_higher_salary(self) -> str:
        return self.get_sql_cmd("db_select_vacancies_with_higher_salary.sql")

    def get_command_db_select_vacancies_with_keywords(self) -> str:
        return self.get_sql_cmd("db_select_vacancies_with_keyword.sql")

    def get_sql_cmd(self, filename: str) -> str:
        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        abs_file_path = os.path.join(script_dir, filename)
        return open(abs_file_path, "r", encoding="utf-8").read()

    def create_db(self) -> bool:
        # Из-за особенностей обратки команды CREATE DATABASE
        # нужно по особенному подключаться к СУБД
        # и обязательно БЕЗ контекстного менеджера
        operation_result = True
        config = self.load_config_without_db()
        self.connect(config)
        self.__conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cur = self.__conn.cursor()
        try:
            cmd = self.get_command_db_create()
            cur.execute(cmd)
        except psycopg2.errors.DuplicateDatabase as e:
            print(e)
        except Exception as e:
            print(e)
            operation_result = False

        self.__conn.close()
        return operation_result

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        with self.__conn.cursor() as cur:
            cur.execute(self.get_command_db_select_companies_and_vacancies())
            print("!!! Select companies and vacancies count")
            return cur.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        with self.__conn.cursor() as cur:
            cur.execute(self.get_command_db_select_all_vacancies())
            print("!!! Select all vacancies")
            return cur.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        with self.__conn.cursor() as cur:
            cur.execute(self.get_command_db_select_avg_salary())
            print("!!! Select avg salary")
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with self.__conn.cursor() as cur:
            cur.execute(self.get_command_db_select_vacancies_with_higher_salary())
            print("!!! Select vacancies with higher salary")
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keywords: list | tuple):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        with self.__conn.cursor() as cur:
            cur.execute(self.get_sql_cmd("db_create_pattern_table.sql"))
            for k in keywords:
                cur.execute(self.get_sql_cmd("db_insert_into_pattern_table.sql"), (f"%{k}%".lower(), ))

            cur.execute(self.get_command_db_select_vacancies_with_keywords())
            print("!!! Select vacancies with keywords")
            return cur.fetchall()
