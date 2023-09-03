from datetime import date, datetime
from collections import defaultdict

days_name = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
    }


def get_birthdays_per_week(users):
    current_date = date.today()
    
    greets_list = defaultdict(list)

    for user in users:

        if current_date.year == user['birthday'].year:

            user_bd_weekday = user['birthday'].weekday()
            
            if current_date.month > user['birthday'].month:
                pass
            elif current_date.month == user['birthday'].month:
                if current_date.day > user['birthday'].day:
                    pass
                else:
                    if user_bd_weekday in (5, 6):  
                        greets_list[days_name[0]].append(user['name'])
                    else:
                        greets_list[days_name[user_bd_weekday]].append(user['name'])

            else:
                if user_bd_weekday in (5, 6):
                    greets_list[days_name[0]].append(user['name'])
                else:
                    greets_list[days_name[user_bd_weekday]].append(user['name'])

        elif current_date.year < user['birthday'].year:
            if user_bd_weekday in (5, 6):
                greets_list[days_name[0]].append(user['name'])
            else:
                greets_list[days_name[user_bd_weekday]].append(user['name'])

        else:
            user.update({'birthday': datetime(year=current_date.year + 1, month=user['birthday'].month, day=user['birthday'].day).date()})
            if (current_date - user['birthday']).days <= 7: 
                user_bd_weekday = user['birthday'].weekday()
                greets_list[days_name[user_bd_weekday]].append(user['name'])

    return greets_list


if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 1, 1).date()},
    ]

    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
