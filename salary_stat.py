import hh_parser
import superjob_parser
import argparse
from statistics import mean
from terminaltables import AsciiTable
from dotenv import load_dotenv
import os


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Count mean salary for developers'
    )
    parser.add_argument(
        '-l', '--lang_list',
        default='python',
        type=str,
        nargs='+',
        help='programming languages for comparison',
    )
    parser.add_argument(
        '-p', '--search_period',
        default=30,
        type=int,
        help='the maximum allowed period of time from the moment of opening'
                ' a vacancy (in days)',
    )
    return parser.parse_args()


def calc_mean_salary_for_speciality(speciality_salaries, koef_from = 1.2, 
                                    koef_to = 0.8):
    mean_salaries = []
    for item in speciality_salaries:
        if not item["salary_currency"] in ("RUR", "rub"):
            continue
        if item["salary_from"] is None and item["salary_to"] is None:
            continue
        if item["salary_from"] is None:
            mean_salaries.append(float(item["salary_to"]) * koef_to)
            continue
        if item["salary_to"] is None:
            mean_salaries.append(float(item["salary_from"]) * koef_from) 
            continue
        mean_salaries.append(
            mean([
                float(item["salary_to"]), 
                float(item["salary_from"])
            ])
        )              
    return (len(mean_salaries), mean(mean_salaries))


def create_salary_stat_object(lang, vacancies_with_salary):
    salary_data = {}
    salary_data["lang"] = lang
    salary_data["vacancies found"] = len(vacancies_with_salary)
    (count, mean_salary) = calc_mean_salary_for_speciality(vacancies_with_salary)
    salary_data["vacancies processed"] = count
    salary_data["mean salary"] = round(mean_salary)
    return salary_data


def pretty_print(title, salaries_data):
    print()
    table_data = []
    table_data.append([
        'Язык программирования', 
        'Найдено вакансий', 
        'Обработано вакансий', 
        'Средняя зарплата, руб.'
    ])
    for salary_data in salaries_data:
        table_data.append([
            salary_data["lang"],
            salary_data["vacancies found"],
            salary_data["vacancies processed"],
            salary_data["mean salary"],        
        ])
    table = AsciiTable(table_data, title)
    print(table.table) 
    print()


def main():
    args = parse_arguments()
    load_dotenv()
    sj_key = os.getenv("SECRET_KEY") 
    hh_salaries_stat = []
    sj_salaries_stat = []    
    vacancy_template = "Разработчик"
    for lang in args.lang_list:
        vacancy_name = '{0} {1}'.format(vacancy_template, lang)
        print("Searching for '{0}' in HeadHunter...".format(vacancy_name))
        try:
            hh_vacancies_with_salary = hh_parser.get_salary_data(
                vacancy_name,
                period_int=args.search_period
            )
            hh_salaries_stat.append(create_salary_stat_object(lang, 
                                                hh_vacancies_with_salary))
        except requests.exceptions.HTTPerror as error:
            print("Can't get data from HeadHunter with error:\n {0}".format(
                                                                    error))            
        print("Searching for '{0}' in SuperJob...".format(vacancy_name))
        try:
            sj_vacancies_with_salary = superjob_parser.get_salary_data(
                vacancy_name,
                sj_key,
                period_int=args.search_period
            )
            sj_salaries_stat.append(create_salary_stat_object(lang, 
                                                    sj_vacancies_with_salary))            
        except requests.exceptions.HTTPerror as error:
            print("Can't get data from SuperJob with error:\n {0}".format(error))
    pretty_print('HeadHunter', hh_salaries_stat)
    pretty_print('SuperJob', sj_salaries_stat)    
        

if __name__ == '__main__':
    main()