import sys,os, datetime
from api.logger.logger import console_logger
from dateutil import tz

class ErrorHandler:

    def __init__(self) -> None:
        pass

    def convert_to_utc_format(self,date_time, format, timezone= "Asia/Kolkata",start = True):
        to_zone = tz.gettz(timezone)
        _datetime = datetime.datetime.strptime(date_time, format)

        if not start:
            _datetime =_datetime.replace(hour=23,minute=59)
        return _datetime.replace(tzinfo=to_zone).astimezone(datetime.timezone.utc).replace(tzinfo=None)

    def error_handler(self, e):
        console_logger.debug(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        console_logger.debug((exc_type, fname, exc_tb.tb_lineno))
        console_logger.debug("Error {} on line {} ".format(e, sys.exc_info()[-1].tb_lineno))
        return e
    
helpers=ErrorHandler()
