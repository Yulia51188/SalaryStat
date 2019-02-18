import requests
import argparse


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


def get_vacancies_page(url, params, page_index):
    params_with_page = params
    params_with_page["page"] = page_index
    response = requests.get(url, params=params_with_page)
    if response.ok:
        return response.json()
        print("Get page #{0}".format(page_index))
    else:
        return None
        print("Can't get page #{0}".format(page_index))       


def get_vacancies(vacancy_name, hh_url="https://api.hh.ru/vacancies", area="1", 
                only_with_salary="true", period="30"):
    params = {
        "text": vacancy_name,
        "area": area,
        "only_with_salary": only_with_salary,
        "period": period,
    }    
    response = requests.get(hh_url, params=params)
    response_data= response.json()
    page_number = response_data["pages"]    
    response_data_list = [get_vacancies_page(hh_url, params, index) 
                            for index in range(0,page_number)]
    return response_data_list


def join_vacancies_pages(data_pages):
    vacancy_list = []
    for data_page in data_pages:
        for item in data_page["items"]:
            vacancy_list.append(item)
    return vacancy_list


def get_salary_data(vacancy_name, period="30"):
    data_pages = get_vacancies(vacancy_name, period=period)
    vacancies = join_vacancies_pages(data_pages)
    salary_data = []
    for vacancy in vacancies:
        salary_data.append({
            "id": vacancy["id"],
            "name": vacancy["name"],
            "salary": vacancy["salary"],
        })
    return salary_data


def main():
    args = parse_arguments()
    vacancy_name = ' '.join(args.vacancy_name)
    search_period = str(args.search_period)
    salary = get_salary_data (vacancy_name, 
        period=search_period)
    print(salary)


if __name__ == '__main__':
    main()