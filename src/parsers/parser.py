from abc import ABC, abstractmethod

from src.vacancy import VacanciesList


class Parser(ABC):

    @abstractmethod
    def load_vacancies(self, keywords: list[str], salary: int, number_of_vacation: int):
        pass

    @property
    @abstractmethod
    def vacancies(self) -> VacanciesList:
        pass
