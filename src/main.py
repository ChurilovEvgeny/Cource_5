# 5865644 ООО ПЕТЕРБУРГСКИЙ ЗАВОД ИЗМЕРИТЕЛЬНЫХ ПРИБОРОВ
# 679023 ООО Спецпроект
# 3007832 ООО Газпром СПГ технологии

from src.parsers.hh_employers import HHEmployers
from src.parsers.hh import HH
from src.sql.dbmanager import DBManager


def main():
    hhe = HHEmployers()
    hhe.load_employer_info([5865644, 679023, 3007832])
    print(hhe.employers)

    hhv = HH()
    hhv.load_vacancies([5865644, 679023, 3007832])
    print(hhv.vacancies)

    return

    db = DBManager()
    db.create_db()
    with db.connect(db.load_config()) as conn:
        with conn.cursor() as cur:
            cur.execute(db.get_command_sql_is_tables_exists())
            if not int(cur.fetchone()[0]):
                cur.execute(db.get_command_sql_init())

        with conn.cursor() as cur:
            ls = hhe.employers.to_list()
            for emp_info in ls:
                cur.execute(db.get_command_sql_insert_into_employers(), emp_info)

    conn.close()


if __name__ == "__main__":
    main()
