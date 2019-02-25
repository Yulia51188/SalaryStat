import requests
import argparse
from itertools import count


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Get vacancies from Head Hunter by vacancy name'
    )
    parser.add_argument(
        '-n', '--vacancy_name',
        default='программист',
        type=str,
        nargs='+',
        help='necessary vacancy name, default is "программист"',
    )
    parser.add_argument(
        '-p', '--search_period',
        default=30,
        type=int,
        help='the maximum allowed period of time from the moment of opening'
                ' a vacancy (in days)',
    )
    return parser.parse_args()


def get_page_with_vacancies(url, params, page_index):
    params_with_page = params
    params_with_page["page"] = page_index
    response = requests.get(url, params=params_with_page)
    response.raise_for_status()
    if response.ok:
        return response.json()
  

def fetch_all_pages_with_vacancies(vacancy_name, hh_url="https://api.hh.ru/vacancies", area="1", 
                only_with_salary="true", period="30"):
    params = {
        "text": vacancy_name,
        "area": area,
        "only_with_salary": only_with_salary,
        "period": period,
    }    
    for page_index in count(start=0):
        data_page = get_page_with_vacancies(hh_url, params, page_index)
        yield from data_page["items"]
        if page_index >= data_page["pages"] :
            break  


def get_salary_data(vacancy_name, period_int=30):
    vacancies = list(fetch_all_pages_with_vacancies(vacancy_name, period=str(period_int)))
    salary_data = []
    for vacancy in vacancies:
        salary_data.append({
            "id": vacancy["id"],
            "name": vacancy["name"],
            "salary_from": vacancy["salary"]["from"],
            "salary_to": vacancy["salary"]["to"],
            "salary_currency": vacancy["salary"]["currency"],
        })
    return salary_data


def main():
    args = parse_arguments()
    vacancy_name = ' '.join(args.vacancy_name)
    try:
        salary = get_salary_data (vacancy_name, period_int=search_period)
        print(salary)        
    except requests.exceptions.HTTPerror as error:
        print("Can't get data from HeadHunter with error:\n {0}". format(error))



if __name__ == '__main__':
    main()