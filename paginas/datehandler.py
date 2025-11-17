from calendar import monthcalendar, monthrange
from typing import List

class DateHandler:
    """
    Obtains and organizes routine calendar data
    Static Methods:
        date_list( year: int, month: int) -> list[int]     Returns flattened monthcalendar matrix
        days_in_month(month:int, year:int) -> int          Returns number of days in given month
        month_num_to_string(month: int) -> str            Returns month name from numerical representation
    """
    @staticmethod
    def date_list(year: int, month: int) -> List[int]:
        """
        Flattens monthcalendar matrix
        Parameters:
            year: year represented numerically
            month: month represented numerically
        Returns:
            Returns a list representing a month’s calendar. Days outside the month are represented by zeros. Each week begins with Monday
        """
        month_calendar = monthcalendar(year, month)
        return [date_num for sublist in month_calendar for date_num in sublist]

    @staticmethod
    def days_in_month(month: int, year: int) -> int:
        """
        Returns number of days in a given month/year
        Parameters:
            month: month represented numerically
            year:  year represented numerically
        Returns: int equal to number of days in given month
        """
        return monthrange(year, month)[1]

    @staticmethod
    def month_num_to_string(month: int) -> str:
        """
        Diccionario para transformar número del mes en nombre
        Parametros:
            month: mes representado numericamente
        Returns: mes representado por nombre
        """
        month_dict = {1: "ENERO", 2: "FEBRERO", 3: "MARZO", 4: "ABRIL", 5: "MAYO", 6: "JUNIO", 7: "JULIO",
                      8: "AGOSTO", 9: "SEPTIEMBRE", 10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE"}
        return month_dict[month]
