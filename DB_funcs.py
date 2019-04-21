import os
import datetime
import csv
import re

from animation_config import *


class FranchiseData:
    def __init__(self, franchise_name):
        self.franchise_name         = franchise_name[0:-4]
        self.date_array             = []
        self.film_name_array        = []
        self.daily_gross_array      = []
        self.gross_to_date_array    = [0]
        self.adjusted_daily_gross   = []
        self.adjusted_gtd           = [0]


def get_earliest_date(franchise_data_array):
    earliest_date = datetime.datetime(year=2100, month=1, day=1)
    for franchise_data in franchise_data_array:
        if franchise_data.date_array[0] < earliest_date:
            earliest_date = franchise_data.date_array[0]


def make_film_name_succinct(film_name):
    for string in DISPOSABLE_STRINGS:
        if string in film_name:
            return film_name.replace(string, "")
    return film_name


def make_franchise_name_succinct(franchise_name):
    ret_val = franchise_name
    if franchise_name in FRANCHISE_NAME_DICT:
        ret_val = FRANCHISE_NAME_DICT[franchise_name]
    ret_val = ret_val + ": "
    return "     " + ret_val.ljust(20)


def read_db(num_of_lines=10000):
    franchise_data_array = []
    list_of_db_files = os.listdir("DB//")

    inflation_dict = {}
    with open("InflationDB.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_line = csv_file.readline()
        for row in csv_reader:
            year_and_month = row[0]
            dollar_value = float(row[1])
            inflation_dict[year_and_month] = dollar_value

    for file in list_of_db_files:
        franchise_data = FranchiseData(file)
        file_path = "DB//" + file
        with open(file_path, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_line = csv_file.readline()
            for i, row in enumerate(csv_reader):
                if i > num_of_lines:
                    break
                # print(row)
                date = datetime.datetime.strptime(row[1], '%Y-%m-%d')
                franchise_data.date_array.append(date)

                year_and_month = row[1][0:4] + row[1][5:7]
                if year_and_month in inflation_dict:
                    dollar_value = inflation_dict[year_and_month]
                else:
                    dollar_value = 1

                daily_gross = int(re.sub('[$,]', '', row[2])) / 10 ** 9 # Fix dollars to billions of dollars
                adjusted_daily_gross = daily_gross * dollar_value
                franchise_data.daily_gross_array.append(daily_gross)
                franchise_data.adjusted_daily_gross.append(adjusted_daily_gross)

                gtd = franchise_data.gross_to_date_array[-1] + daily_gross
                adjusted_gtd = franchise_data.adjusted_gtd[-1] + adjusted_daily_gross
                franchise_data.gross_to_date_array.append(gtd)
                franchise_data.adjusted_gtd.append(adjusted_gtd)

                film_name = row[0]
                if SHORTEN_FILM_NAMES:
                    film_name = make_film_name_succinct(film_name)
                franchise_data.film_name_array.append(film_name)

        franchise_data.gross_to_date_array.pop(0)
        franchise_data.adjusted_gtd.pop(0)
        franchise_data_array.append(franchise_data)

    return franchise_data_array
