from http import HTTPStatus

import requests

from src.vacancy import VacanciesList, Vacancy


class HHVacancies:
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self):
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100}
        self.__vacancies = VacanciesList()

    def load_vacancies(self, employers_id: list[int] | tuple):
        """
        Загрузить вакансии с hh.ru
        :param employers_id: список идентификаторов работодателей
        :return: None
        """

        for emp_id in employers_id:
            self.__params['employer_id'] = str(emp_id)
            self.__params['page'] = 0
            self.__params['per_page'] = 100
            while True:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                if response.status_code != HTTPStatus.OK:
                    break

                resp_json = response.json()
                if 'items' not in resp_json:
                    break

                vac_json = response.json()['items']
                [self.__vacancies.append(Vacancy(**vac)) for vac in vac_json]

                cur_page = int(response.json()['page'])
                count_pages = int(response.json()['pages'])

                if cur_page < count_pages - 1:
                    self.__params['page'] += 1
                else:
                    break

    @property
    def vacancies(self) -> VacanciesList:
        return self.__vacancies
