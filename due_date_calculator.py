import re
import math


class CustomError(Exception):
    pass


def validate_input(user_input):
    # Regex that validates the given yyyy.mm.dd hh:mm datetime format and 9AM - 5PM
    date_regex = re.compile(
        r'(((\d{4})(.)(0[13578]|10|12)(.)(0[1-9]|[12][0-9]|3[01]))|((\d{4})(.)(0[469]|11)(.)([0][1-9]|[12][0-9]|30))|((\d{4})(.)(02)(.)(0[1-9]|1[0-9]|2[0-8]))|(([02468][048]00)(.)(02)(.)(29))|(([13579][26]00)(.)(02)(.)(29))|(([0-9][0-9][0][48])(.)(02)(.)(29))|(([0-9][0-9][2468][048])(.)(02)(.)(29))|(([0-9][0-9][13579][26])(.)(02)(.)(29)))(\s(09|1[0-7]):([0-5][0-9]))'
    )
    res = date_regex.fullmatch(user_input)
    if res is None:
        raise CustomError("InvalidDateException")


def calculate_weekday(user_input):
    split_input = user_input.split(" ")
    date = split_input[0]
    split_date = date.split(".")
    date_time = {}
    date_time["year"] = int(split_date[0])
    date_time["month"] = int(split_date[1])
    date_time["day"] = int(split_date[2])

    # Required month shifting for the doomsday algorithm
    if date_time["month"] < 3:
        date_time["year"] -= 1
        date_time["month"] += 10
    else:
        date_time["month"] -= 2

    century = math.floor(date_time["year"]/100)
    year = date_time["year"] - century*100

    # Doomsday algorithm
    weekday_nr = (date_time["day"] + math.floor(2.6*date_time["month"] - 0.2) - 2*century +
                  year + math.floor(year/4) + math.floor(century/4)) % 7

    day_names = ["Sunday", "Monday", "Tuesday",
                 "Wednesday", "Thursday", "Friday", "Saturday"]

    date_time["weekday_nr"] = weekday_nr
    date_time["weekday_name"] = day_names[weekday_nr]
    return date_time


def read_date():
    print("Please provide a submit date (yyyy.mm.dd hh:mm format):")
    user_input = input()
    validate_input(user_input)
    weekday = calculate_weekday(user_input)
    if weekday == "Saturday" or weekday == "Sunday":
        raise CustomError("Cannot submit on weekends!")
    return weekday


def main():
    read_date()


if __name__ == '__main__':
    main()
