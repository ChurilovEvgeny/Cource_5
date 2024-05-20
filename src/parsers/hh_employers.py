from http import HTTPStatus

import requests

from src.employer import EmployersList, Employer


class HHEmployers:
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self):
        self.__url = 'https://api.hh.ru/employers/'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100}
        self.__employers = EmployersList()

    def load_employer_info(self, employers_id: list[int]):
        """
        Загрузить информацию о работодателях с hh.ru
        :param employers_id: список идентификаторов работодалей
        :return: None
        """

        for e_id in employers_id:
            url = self.__url + str(e_id)
            response = requests.get(url, headers=self.__headers, params=self.__params)
            if response.status_code != HTTPStatus.OK:
                break

            resp_json = response.json()
            self.__employers.append(Employer(**resp_json))

    @property
    def employers(self) -> EmployersList:
        return self.__employers
