from pydantic import BaseModel, PositiveInt, AnyHttpUrl, RootModel


class Employer(BaseModel):
    """
    Класс контейнер Работодателя. Требуемые ИМЕНОВАННЫЕ параметры:\n
    - id: PositiveInt
    - name: str
    - alternate_url: AnyHttpUrl
    """
    id: PositiveInt
    name: str
    alternate_url: AnyHttpUrl

    def __str__(self):
        return (f"{30 * '*'}\n"
                f"id: {self.id}\n"
                f"Работодатель: {self.name}\n"
                f"URL: {self.alternate_url}\n")

    def to_tuple(self):
        return self.id, self.name, str(self.alternate_url)


class EmployersList(RootModel):
    """
    Класс контейнер списка работодателей. Требуемые параметры:\n
    - list[Vacancy] = None
    """
    root: list[Employer] = []

    def append(self, employer: Employer):
        """
        Добавляет объект типа Employer, описывающий работодателя в списке работодателей
        :param employer: Работодатель
        :return: None
        """
        self.root.append(employer)

    def to_list(self):
        return [e.to_tuple() for e in self.root]

    def __str__(self):
        return "Нет данных!" if not self.root else "\n".join(map(str, self.root))
