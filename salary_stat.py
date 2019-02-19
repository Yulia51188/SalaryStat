import hh_parser
import argparse
from statistics import mean
from terminaltables import AsciiTable


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
    hh_salaries_data = []
    sj_salaries_data = []    
    search_period = str(args.search_period)
    vacancy_template = "Программист"
    for index, lang in enumerate(args.lang_list):
        vacancy_name = ' '.join([vacancy_template, lang])
        print("Searching for '{0}' in HeadHunter...".format(vacancy_name))
        hh_vacancies_with_salary = hh_parser.get_salary_data(     
            vacancy_name,
            period=search_period,
        )
        hh_salaries_data.append(create_salary_stat_object(lang, 
                                                    hh_vacancies_with_salary))
        #TO DO: debug superjob parsing
        print("Searching for '{0}' in SuperJob...".format(vacancy_name))
        sj_vacancies_with_salary = superjob_parser.get_salary_data(     
             vacancy_name,
             period=search_period,
         )
        sj_salaries_data.append(create_salary_stat_object(lang, 
                                                    sj_vacancies_with_salary))
    pretty_print('HeadHunter', hh_salaries_data)
    pretty_print('SuperJob', sj_salaries_data)    
        

if __name__ == '__main__':
    main()