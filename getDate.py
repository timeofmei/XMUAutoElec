import time
import datetime


def getDateData():
    data = {}
    today = datetime.datetime.today()
    # startDate
    dateStart = str(today.year) + "年" + str(today.month) + "月01日"
    structDateStart = datetime.datetime(
        today.year, today.month, 1, 8).timetuple()
    dateStartObj = datetime.datetime(
        today.year, today.month, 1)
    dateStartDDDC = dateStartObj.strftime(r"%m/%d/%Y")
    data["dxdateStart_Raw"] = str(
        int(time.mktime(structDateStart))) + "000"
    data["dxdateStart"] = dateStart
    data["dxdateStart$DDD$C"] = dateStartDDDC + ":" + dateStartDDDC
    # endDate
    dateEnd = str(today.year) + "年" + str(today.month) + \
        "月" + str(today.day) + "日"
    structDateEnd = datetime.datetime(
        today.year, today.month, today.day, 8).timetuple()
    dateEndObj = datetime.datetime(
        today.year, today.month, today.day)
    dateEndDDDC = dateEndObj.strftime(r"%m/%d/%Y")
    data["dxdateEnd"] = dateEnd
    data["dxdateStart_Raw"] = str(
        int(time.mktime(structDateEnd))) + "000"
    data["dxdateEnd$DDD$C"] = dateEndDDDC + ":" + dateEndDDDC
    return data
