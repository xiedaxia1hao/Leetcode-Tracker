import requests
import xlwt
from bs4 import BeautifulSoup
URL_PATTERN = 'https://leetcode.jp/problems.php?page_index={}&sort=0000&keyword=&company={}'


def get_data(company_list):
    question_dict_breakdown_by_company = {}
    for company in company_list:
        question_dict_breakdown_by_company.setdefault(company, [])
        data_sheet = data_excel.add_sheet(company)
        row = 0
        page_number = 1
        tr_tags = ['dummy_tag_1', 'dummy_tag_2']
        while len(tr_tags) > 1:
            url = URL_PATTERN.format(page_number, company)
            print(url)
            html_doc = requests.get(url).content.decode('utf-8')
            soup = BeautifulSoup(html_doc, 'html.parser')
            tr_tags = soup.find_all('tr')
            for tr_tag in tr_tags:
                text = str.splitlines(tr_tag.text)
                if len(text) == 5:
                    question_num = text[1]
                    name = text[2]
                    difficulty = text[3]
                    lock_status = text[4]
                    print('{} - {} - {} - {}'.format(question_num, name, difficulty, lock_status))
                    question_dict_breakdown_by_company.get(company).append(question_num)
                    question_info_dict[question_num] = (question_num, name, difficulty, lock_status)
                    data_sheet.write(row, 0, question_num)
                    data_sheet.write(row, 1, name)
                    data_sheet.write(row, 2, difficulty)
                    data_sheet.write(row, 3, lock_status)
                    row += 1
            page_number += 1
    return question_dict_breakdown_by_company


def intersect_questions(question_dict_breakdown_by_company):
    question_ids_by_company = list(question_dict_breakdown_by_company.values())
    result = set(question_ids_by_company[0])
    for ids in question_ids_by_company:
        result.intersection_update(set(ids))

    row = 0
    data_sheet = data_excel.add_sheet('Intersection')
    for id in sorted(result, key=int):
        question_info = question_info_dict.get(id)
        data_sheet.write(row, 0, question_info[0])
        data_sheet.write(row, 1, question_info[1])
        data_sheet.write(row, 2, question_info[2])
        data_sheet.write(row, 3, question_info[3])
        row += 1


data_excel = xlwt.Workbook()
question_info_dict = {}
if __name__ == '__main__':
    company_list = ['Amazon', 'Google', 'Facebook']
    # company_list = ['LinkedIn', 'Yahoo']
    question_dict_breakdown_by_company = get_data(company_list)
    intersect_questions(question_dict_breakdown_by_company)
    data_excel.save('./lc_questions.xls')
