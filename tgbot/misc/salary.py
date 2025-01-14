async def salary_with_percents(
        hourly_payment: float,
        hours_worked: int,
        aht: int = 0,
        flr: int = 0,
        gok: int = 0,
        premium_percent: int = 0,
        client_rating: int = 0,
        tests: str = 0,
        sl: int = 0,
        acknowledgments: int = 0,
        mentoring_type: str = "",
        mentoring_days: float = 0,
):
    if premium_percent == 0:
        hours_salary = round(hourly_payment * hours_worked, 2)
        premium_percent = aht + flr + gok
        tests = 5 if tests == "yes" else 0
        premium_percent += tests + client_rating + acknowledgments
        if mentoring_type != "":
            if mentoring_type == "3d":
                mentoring = mentoring_days * 0.5
            elif mentoring_type == "main":
                mentoring = mentoring_days * 1
            else:
                mentoring = mentoring_days * 1.5
            premium_percent += mentoring
        premium_salary = round(hours_salary * (premium_percent / 100), 2)
        salary_sum = round(hours_salary + premium_salary, 2)

        salary = {
            "hours_salary": hours_salary,
            "premium_percent": premium_percent,
            "premium_salary": premium_salary,
            "salary_sum": salary_sum,
        }
    else:
        hours_salary = round(hourly_payment * hours_worked, 2)
        premium_percent = premium_percent
        premium_salary = round(hours_salary * (premium_percent / 100), 2)
        salary_sum = round(hours_salary + premium_salary, 2)

        salary = {
            "hours_salary": hours_salary,
            "premium_percent": premium_percent,
            "premium_salary": premium_salary,
            "salary_sum": salary_sum,
        }
    return salary


async def vacation_pay(
        total_year_salary: float,
        vacation_days_count: int = 14,
        calendar_days_in_period: float = 351.6,
):
    vacation_salary = round(
        total_year_salary / calendar_days_in_period * vacation_days_count, 2
    )
    return vacation_salary
