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
        mean_salaries.append(mean([
            float(item["salary"]["to"]), 
            float(item["salary"]["from"])
        ]
        ))              
    return mean(mean_salaries)


def main():
    args = parse_arguments()
    vacancy_temlate = 'программист'
    salaries_data = []
    for index, lang in enumerate(args.lang_list):
        vacancy_name = ' '.join([vacancy_temlate, lang])
        print("Searching for '{0}'...".format(vacancy_name))
        search_period = str(args.search_period)
        salaries_data.append({})
        salaries_data[index]["lang"] = lang
        salaries_data[index]["items"] = hh_parser.get_salary_data(
            hh_parser.get_vacancies(
                vacancy_name, 
                period=1
            )
        )
        print("For '{0}' found {1} vacancies".format(
            vacancy_name, 
            len(salaries_data[index]["items"]))
        )
    print("Search completed. Results:")
    for salary_data in salaries_data:
        #print("{0} - {1} vacancies".format(salary_data["lang"], len(salary_data["items"])))
        salary_data["mean_salary"] = calc_mean_salary_for_speciality(
            salary_data["items"]
        )

    for salary_data in salaries_data:
        print("{0} - {1} vacancies - {2} RUR".format(
            salary_data["lang"], 
            len(salary_data["items"]),
            salary_data["mean_salary"],
            )
        )
       

if __name__ == '__main__':
    main()