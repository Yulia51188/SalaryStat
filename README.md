# SalaryStat
The script `salary_stat.py` compares mean salaries of developers of different programming languages. The list of languages you can input as arguments of command line (see example in section 'How to launch').
- To get salary data  from [HeadHunter](https://hh.ru/) and [SuperJob](https://www.superjob.ru/) it uses functions `def get_salary_data(vacancy_name, period_int=30)` from unit `hh_parser.py` and `def get_salary_data(vacancy_name, key, period_int=30)` from `superjob_parser.py`. 
- Then function `create_salary_stat_object(lang, vacancies_with_salary)` make a list of dictionaries with statistics for each programming language (language, vacancies found, vacancies proccessed, mean salary)
- Finally, function `pretty_print(title, salaries_data)` print table with salary data for developers vacancies for all input languages.

# How to install

To get vacancies from SuperJob you need to have '.env' file with API SECRET_KEY. You can get it after registration in [SuperJob](https://api.superjob.ru/register/). 

Python3 should be already installed. Then use pip3 (or pip) to install dependencies:
```bash
pip3 install -r requirements.txt
```
# How to launch

Example of the launch of `salary_stat.py` in Linux (with python 3.5):

```bash
$ python3 salary_stat.py -l python java
Searching for 'Разработчик python' in HeadHunter...
Searching for 'Разработчик python' in SuperJob...
Searching for 'Разработчик java' in HeadHunter...
Searching for 'Разработчик java' in SuperJob...

+HeadHunter-------------+------------------+---------------------+------------------------+
| Язык программирования | Найдено вакансий | Обработано вакансий | Средняя зарплата, руб. |
+-----------------------+------------------+---------------------+------------------------+
| python                | 409              | 376                 | 145217                 |
| java                  | 492              | 462                 | 157965                 |
+-----------------------+------------------+---------------------+------------------------+


+SuperJob---------------+------------------+---------------------+------------------------+
| Язык программирования | Найдено вакансий | Обработано вакансий | Средняя зарплата, руб. |
+-----------------------+------------------+---------------------+------------------------+
| python                | 21               | 21                  | 60000                  |
| java                  | 10               | 10                  | 88000                  |
+-----------------------+------------------+---------------------+------------------------+
```
To see all input arguments use `--help`:
```bash
$ python3 salary_stat.py --help
usage: salary_stat.py [-h] [-l LANG_LIST [LANG_LIST ...]] [-p SEARCH_PERIOD]

Count mean salary for developers

optional arguments:
  -h, --help            show this help message and exit
  -l LANG_LIST [LANG_LIST ...], --lang_list LANG_LIST [LANG_LIST ...]
                        programming languages for comparison
  -p SEARCH_PERIOD, --search_period SEARCH_PERIOD
                        the maximum allowed period of time from the moment of
                        opening a vacancy (in days)
```
# Project Goals

The code is written for educational purposes on online-course for web-developers dvmn.org.
