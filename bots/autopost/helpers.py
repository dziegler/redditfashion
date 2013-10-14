DAY_SUFFIX = {
    1: 'st',
    2: 'nd',
    3: 'rd',
    21: 'st',
    22: 'nd',
    23: 'rd',
    31: 'st'
}

def day_suffix(date):
    return DAY_SUFFIX.get(date.day, "th")

def custom_strftime(format, date):
    return date.strftime(format).format(day_suffix=day_suffix(date))
