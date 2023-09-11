import datetime


class DatetimeManager:
    def __init__(self):
        self.datetime = datetime.datetime.now()

    def get_datetime_string(self) -> str:
        return self.datetime.strftime('%d/%m/%Y')

    def get_part_of_the_day(self) -> str:
        current_hour = self.datetime.hour

        part_of_the_day = ""
        if 5 <= current_hour < 12:
            part_of_the_day = 'Morning'
        elif 12 <= current_hour < 17:
            part_of_the_day = 'Afternoon'
        elif 17 <= current_hour < 21:
            part_of_the_day = 'Evening'
        else:
            part_of_the_day = 'Night'

        return part_of_the_day
