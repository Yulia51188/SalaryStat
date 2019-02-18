import hh_parser
import argparse
from statistics import mean


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
        if not item["salary"]["currency"] == "RUR":
            continue
        if item["salary"]["from"] is None and item["salary"]["to"] is None:
            continue
        if item["salary"]["from"] is None:
            mean_salaries.append(float(item["salary"]["to"]) * koef_to)
            continue
        if item["salary"]["to"] is None:
            mean_salaries.append(float(item["salary"]["from"]) * koef_from) 
            continue
        mean_salaries.append(
            mean([
                float(item["salary"]["to"]), 
                float(item["salary"]["from"])
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


def main():
    args = parse_arguments()
    salaries_data = []
    search_period = str(args.search_period)
    vacancy_template = "Программист"
    for index, lang in enumerate(args.lang_list):
        vacancy_name = ' '.join([vacancy_template, lang])
        print("Searching for '{0}'...".format(vacancy_name))
        vacancies_with_salary = hh_parser.get_salary_data(     
            vacancy_name,
            period=search_period,
        )
        salaries_data.append(create_salary_stat_object(lang, 
                                                    vacancies_with_salary))
    for salary_data in salaries_data:
        print()
        for key in sorted(salary_data):
            print('{key}: {value}'.format(key=key, value=salary_data[key]))
        

if __name__ == '__main__':
    main()