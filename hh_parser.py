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
    #print("Total: {0}".format(page_number))
    response_data_list = [get_vacancies_page(hh_url, params, index) for index in range(0,page_number)]
    return response_data_list


def main():
    args = parse_arguments()
    vacancy_name = ' '.join(args.vacancy_name)
    vacancies = get_vacancies(vacancy_name)
    print("Get {0} pages".format(len(vacancies)))


if __name__ == '__main__':
    main()