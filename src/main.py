# 5865644 ООО ПЕТЕРБУРГСКИЙ ЗАВОД ИЗМЕРИТЕЛЬНЫХ ПРИБОРОВ
# 679023 ООО Спецпроект
# 3007832 ООО Газпром СПГ технологии

from src.parsers.hh_employers import HHEmployers
from src.parsers.hh import HH
from src.sql.dbmanager import DBManager

EMPLOYERS_IDS = (5865644, 679023, 3007832, 1742190, 9473760, 9030164, 990888, 2519536, 10859723, 67611)

def main():

    hhe = HHEmployers()
    hhe.load_employer_info(EMPLOYERS_IDS)
    print(hhe.employers)

    hhv = HH()
    hhv.load_vacancies(EMPLOYERS_IDS)
    print(hhv.vacancies)

    db = DBManager()
    db.create_db()

    db.connect(db.load_config())
    db.init_tables()
    db.insert_employers(hhe.employers.to_list())
    db.insert_vacancies_and_salaries(hhv.vacancies.to_list())

    print(db.get_companies_and_vacancies_count())
    print(db.get_all_vacancies())
    print(db.get_avg_salary())
    print(db.get_vacancies_with_higher_salary())
    print(db.get_vacancies_with_keyword(("главный", "ведущий")))


if __name__ == "__main__":
    main()
