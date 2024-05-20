# 5865644 ООО ПЕТЕРБУРГСКИЙ ЗАВОД ИЗМЕРИТЕЛЬНЫХ ПРИБОРОВ
# 679023 ООО Спецпроект
# 3007832 ООО Газпром СПГ технологии

from src.parsers.hh_employers import HHEmployers
def main():
    hhe = HHEmployers()
    hhe.load_employer_info([5865644, 679023, 3007832])
    [print(i) for i in hhe.employers]


if __name__ == "__main__":
    main()
