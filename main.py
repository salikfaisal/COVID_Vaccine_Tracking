import requests
from bs4 import BeautifulSoup
import math
from datetime import date

today = date.today()
the_day = today.strftime("%B %d %Y").split()
population = 331449281
calender = {'January': 31, 'February': 28, 'March': 31, 'April': 30, 'May': 31, 'June': 30, 'July': 31,
            'August': 31, 'September': 30, 'October': 31, 'November': 30, 'December': 31}
URL = 'https://usafacts.org/visualizations/covid-vaccine-tracker-states/'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
search = soup.find(class_="MuiContainer-root MuiContainer-maxWidthMd").text.strip()
one_dose = int(search[55:66].replace(',', ''))
fully_vaccinated = int(search[140:151].replace(',', ''))
doses_given = int(search[389:400].replace(',', ''))
fully_vaccinated_share_of_total = fully_vaccinated / doses_given

days_since_first_distribution = 11
for month, days_in_month in calender.items():
    if the_day[0] == month:
        days_since_first_distribution += int(the_day[1])
        break
    else:
        days_since_first_distribution += days_in_month

rate_before_decline = 97/2835*1000000*114*fully_vaccinated_share_of_total
doses_since_peak = (doses_given - 194000000)*fully_vaccinated_share_of_total
peak = doses_since_peak / (math.pow((days_since_first_distribution - 113), 0.8) * 1.25 - 1.25)
print("Type '1' if you would like to see the date when __% of people are vaccinated")
print("Type '2' if you would like to see the percentage of people vaccinated on a certain date")
decision = int(input())
while decision != 1 and decision != 2:
    print('Invalid input. Please try again')
    decision = int(input())
else:
    print('Dr. Anthony Fauci estimates that 70% - 85% of the population needs to be vaccinated in order to reach'
          ' herd immunity.\n')
    if decision == 1:
        immunity_percentage = int(input('Enter the percentage of the population vaccinated: ').replace('%', ''))
        total_vaccination_goal = immunity_percentage * population / 100
        if total_vaccination_goal <= 194000000 * fully_vaccinated_share_of_total:
            days_to_goal = math.ceil(math.sqrt(total_vaccination_goal * 5670 / 97000000))
        else:
            vaccinations_after_peak = total_vaccination_goal - 194000000 * fully_vaccinated_share_of_total
            days_to_goal = math.ceil(math.pow(0.8 * (vaccinations_after_peak / peak + 1.25), 1.25) + 113)
        vaccination_goal_date = []
        days_to_goal -= 11
        for month, days_in_month in calender.items():
            if days_to_goal <= days_in_month:
                vaccination_goal_date.append(month)
                vaccination_goal_date.append(days_to_goal)
                break
            days_to_goal -= days_in_month
        print('{}% of the  US population are projected to be fully vaccinated by {} {}, 2021'.format(immunity_percentage,
                                                                                         vaccination_goal_date[0],
                                                                                         vaccination_goal_date[1]))
    else:
        prospective_month = input('Month: ').lower().capitalize()
        prospective_day_in_month = int(input('Day: '))
        days_of_vaccination = 11
        for month, days_in_month in calender.items():
            if prospective_month == month:
                days_of_vaccination += prospective_day_in_month
                break
            days_of_vaccination += days_in_month
        if days_of_vaccination <= 113:
            people_vaccinated = 97000000 * math.pow(days_of_vaccination, 2) / 5670
        else:
            vaccinations_after_peak = peak * (1.25 * math.pow(days_of_vaccination - 113, 0.8) - 1.25)
            people_vaccinated = 194000000 * fully_vaccinated_share_of_total + vaccinations_after_peak
        percentage_vaccinated = round(people_vaccinated / population * 100, 1)
        print('{}% of the  US population are projected to be fully vaccinated by {} {}, 2021'.format(percentage_vaccinated,
                                                                                         prospective_month,
                                                                                         prospective_day_in_month))
    print("\nData from CDC COVID Data Tracker")
