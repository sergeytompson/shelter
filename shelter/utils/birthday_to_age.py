from datetime import date


def convert_birthday_to_age(birthday):
    today = date.today()
    age = (
        today.year
        - birthday.year
        - ((today.month, today.day) < (birthday.month, birthday.day))
    )
    return age
