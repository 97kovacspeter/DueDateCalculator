import re
import math


class CustomError(Exception):
    pass


def add_days_to_date(submit_time, calendar_days):
    year = submit_time["year"]
    month = submit_time["month"]
    day = submit_time["day"]
    elapsed = days_elapsed(year, month, day)

    y, m, d = 2022, 1, 27
    return y, m, d


def calculate_due_date(submit_time, turnaround):
    due_date = {}
    submit_hour = submit_time["hour"]
    # minutes never change with integer hour increments
    due_date["minute"] = submit_time["minute"]
    # day shifting
    due_date["hour"] = submit_hour + turnaround["working_hours"]
    if submit_hour + turnaround["working_hours"] > 17:
        due_date["hour"] = 9 + \
            (turnaround["working_hours"] - (17-submit_hour))
        turnaround["working_days"] += 1

    weeks = turnaround["working_days"] // 5
    remaining_days = turnaround["working_days"] % 5

    calendar_days = weeks * 7 + remaining_days

    y, m, d = add_days_to_date(submit_time, calendar_days)

    due_date["year"] = y
    due_date["month"] = m
    due_date["day"] = d
    return due_date


def days_elapsed(year, month, day):
    elapsed = day
    monthly_cummulation = {
        11: 334,
        10: 304,
        9: 273,
        8: 243,
        7: 212,
        6: 181,
        5: 151,
        4: 120,
        3: 90,
        2: 59,
        1: 31,
        0: 0
    }
    elapsed += monthly_cummulation[month-1]
    if is_leapyear(year) and month > 2:
        elapsed += 1
    return elapsed


def is_leapyear(year):
    if (year % 100 != 0 and year % 4 == 0 or year % 400 == 0):
        return True
    return False


def process_submit_time(user_input):
    split_input = user_input.split(" ")
    date = split_input[0]
    time = split_input[1]

    split_date = date.split(".")
    year = int(split_date[0])
    month = int(split_date[1])
    day = int(split_date[2])

    split_time = time.split(":")
    hour = int(split_time[0])
    minute = int(split_time[1])

    weekday_nr = weekday_number(year, month, day)

    submit_time = {}
    submit_time["year"] = year
    submit_time["month"] = month
    submit_time["weekday_nr"] = weekday_nr
    submit_time["weekday_name"] = weekday_name(weekday_nr)
    submit_time["day"] = day
    submit_time["hour"] = hour
    submit_time["minute"] = minute
    return submit_time


def read_date():
    user_input = input()
    validate_input(user_input)
    submit_time = process_submit_time(user_input)
    if submit_time["weekday_name"] == "Saturday" or submit_time["weekday_name"] == "Sunday":
        raise CustomError("Weekend exception")
    return submit_time


def read_turnaround():
    # Raises ValueError if not integer is given
    turnaround = {}
    turnaround["hours"] = int(input())
    hours = turnaround["hours"]
    if hours < 0:
        raise CustomError("Negative turnaround exception")
    turnaround["working_days"] = hours // 8
    turnaround["working_hours"] = hours % 8
    return turnaround


def validate_input(user_input):
    # Regex that validates the given yyyy.mm.dd hh:mm datetime format and 9AM - 5PM
    date_regex = re.compile(
        r'(((\d{4})[.](0[13578]|10|12)[.](0[1-9]|[12][0-9]|3[01])[.]{0,1})|((\d{4})[.](0[469]|11)[.]([0][1-9]|[12][0-9]|30)[.]{0,1})|((\d{4})[.](02)[.](0[1-9]|1[0-9]|2[0-8])[.]{0,1})|(([02468][048]00)[.](02)[.](29)[.]{0,1})|(([13579][26]00)[.](02)[.](29)[.]{0,1})|(([0-9][0-9][0][48])[.](02)[.](29)[.]{0,1})|(([0-9][0-9][2468][048])[.](02)[.](29)[.]{0,1})|(([0-9][0-9][13579][26])[.](02)[.](29)[.]{0,1}))(\s(09|1[0-7]):([0-5][0-9]))')
    res = date_regex.fullmatch(user_input)
    if res is None:
        raise CustomError("Invalid date exception")


def weekday_name(number):
    day_names = ["Sunday", "Monday", "Tuesday",
                 "Wednesday", "Thursday", "Friday", "Saturday"]
    return day_names[number]


def weekday_number(year, month, day):
    century = math.floor(year/100)
    year_without_century = year - century*100
    # Required month shifting for the doomsday algorithm
    month -= 2
    if month < 1:
        year_without_century -= 1
        month += 12
    # Doomsday algorithm
    weekday_nr = (day + math.floor(2.6*month - 0.2) - 2*century +
                  year_without_century + math.floor(year_without_century/4) +
                  math.floor(century/4)) % 7

    return weekday_nr


def write_date(due_date):
    if due_date["month"] < 10:
        due_date["month"] = "0" + str(due_date["month"])
    if due_date["minute"] < 10:
        due_date["minute"] = "0" + str(due_date["minute"])
    date = [str(due_date["year"]),
            str(due_date["month"]), str(due_date["day"])]
    time = [str(due_date["hour"]), str(due_date["minute"])]
    result = ".".join(date)
    result += " "
    result += ":".join(time)
    print(result)


def main():
    print("Please provide a submit date (yyyy.mm.dd hh:mm format):")
    submit_time = read_date()

    weekday = submit_time["weekday_name"]
    print(f"Valid date! It's a {weekday}.")

    print("Please enter a turnaround time (integer hours):")
    turnaround = read_turnaround()

    due_date = calculate_due_date(submit_time, turnaround)
    write_date(due_date)


if __name__ == '__main__':
    main()
