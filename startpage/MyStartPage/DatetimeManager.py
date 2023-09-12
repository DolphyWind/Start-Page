import datetime


class DatetimeManager:
    def __init__(self):
        self.datetime = datetime.datetime.now()

    @property
    def datetime_string(self):
        self.datetime = datetime.datetime.now()
        return self.datetime.strftime('%d/%m/%Y')

    @property
    def part_of_the_day(self) -> str:
        self.datetime = datetime.datetime.now()
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

    @property
    def clock_initial(self) -> str:
        return self.datetime.strftime('%H:%M:%S')

