# coding=utf-8
"""
ESTIMATOR
"""
from dateutil.relativedelta import relativedelta
from datetime import datetime

registered_types = dict(severe=dict(likely_infected=50), best=dict(likely_infected=10))


#
# def convert_to_days(period_type, time_to_elapse):
#     """
#
#     :param period_type:
#     :param time_to_elapse:
#     :return:
#     """
#     today = datetime.today()
#
#     if 'month' in period_type:
#         delta = relativedelta(months=time_to_elapse)
#     elif 'year' == period_type:
#         delta = relativedelta(years=time_to_elapse)
#     elif 'week' in period_type:
#         delta = relativedelta(weeks=time_to_elapse)
#     else:
#         return 1
#
#     month_from_today = today + delta
#     days = (month_from_today - today).days
#     return days

def convert_to_days(period_type, time_to_elapse):
    """

    :param period_type:
    :param time_to_elapse:
    :return:
    """
    return time_to_elapse * 7 if 'week' in period_type else time_to_elapse * 30


def calculate_impact(data, type_=None):
    """

    :param data:
    :param type_:
    :return:
    """
    type_ = type_ or "best"
    registered_type = registered_types.get(type_, None)
    currently_infected = data.get("reportedCases", 0) * registered_type.get("likely_infected", 0)
    period_type = data.get("periodType", "days")
    time_to_elapse = data.get("timeToElapse", 3)
    days = time_to_elapse if period_type == 'days' else convert_to_days(period_type=period_type,
                                                                        time_to_elapse=time_to_elapse)
    requested_time = 2 ** int(days / 3)

    infections_by_requested_time = int(currently_infected * requested_time)
    severe_cases_by_requested_time = int(0.15 * infections_by_requested_time)
    hospital_beds_by_requested_time = int(
        (0.35 * float(data.get("totalHospitalBeds", 0))) - severe_cases_by_requested_time)

    intense_cases_by_requested_time = int(0.05 * infections_by_requested_time)
    vent_cases_by_requested_time = int(0.02 * infections_by_requested_time)
    region = data.get("region", {})
    avg_daily_income_in_usd = region.get("avgDailyIncomeInUSD", 0)
    avg_daily_income_population = region.get("avgDailyIncomePopulation", 0)
    dollars_in_flight = int(
        ((infections_by_requested_time * avg_daily_income_population) * avg_daily_income_in_usd) / days)

    response = dict(currentlyInfected=currently_infected, infectionsByRequestedTime=infections_by_requested_time,
                    severeCasesByRequestedTime=severe_cases_by_requested_time,
                    hospitalBedsByRequestedTime=hospital_beds_by_requested_time,
                    casesForICUByRequestedTime=intense_cases_by_requested_time,
                    casesForVentilatorsByRequestedTime=vent_cases_by_requested_time,
                    dollarsInFlight=dollars_in_flight)
    return response


def estimator(data):
    """

    :param data:
    :return:
    """
    return dict(data=data, impact=calculate_impact(data), severeImpact=calculate_impact(data, type_='severe'))

# d = estimator({
#     "region": {
#         "name": "Africa",
#         "avgAge": 19.7,
#         "avgDailyIncomeInUSD": 4,
#         "avgDailyIncomePopulation": 0.73
#     },
#     "periodType": "days",
#     "timeToElapse": 38,
#     "reportedCases": 2747,
#     "population": 92931687,
#     "totalHospitalBeds": 678874
# })
