import re
import httpx
from lxml.etree import HTML
from getDate import getDateData


class Elec:
    def __init__(self, xiaoqu, louming, fangjian):
        self.url = "http://elec.xmu.edu.cn/PdmlWebSetup/Pages/SMSMain.aspx"
        self.resp = []
        self.doc = []
        self.finalResult = ""
        self.errmsg = {"账户余额": -2.0, "剩余电量": -2.0}
        self.xiaoqu = xiaoqu
        self.louming = louming
        self.fangjian = fangjian
        self.data = {
            "dxdateStart_DDDWS": "0:0:-1:-10000:-10000:0:-10000:-10000:1",
            "dxdateStart_DDD_C_FNPWS": "0:0:-1:-10000:-10000:0:0px:-10000:1",
            "dxdateEnd_DDDWS": "0:0:-1:-10000:-10000:0:-10000:-10000:1",
            "dxdateEnd_DDD_C_FNPWS": "0:0:-1:-10000:-10000:0:0px:-10000:1"
        }

    def findPat(self, pattern, start=0, end=None, format=str):
        return format(re.compile(pattern).search(self.finalResult).group()[start:end])

    def getElec(self):
        self.getInitPage()
        self.getSquaredPage()
        self.result = self.getFinalResult()
        return self.result

    def getInitPage(self):
        try:
            self.resp.append(httpx.get(self.url))
        except:
            self.result = self.errmsg
            return None
        self.doc.append(HTML(self.resp[0].text))

        self.cookies = self.resp[0].cookies
        self.data["__VIEWSTATE"] = self.doc[0].xpath(
            '//*[@id="__VIEWSTATE"]/@value')[0]
        self.data["__EVENTVALIDATION"] = self.doc[0].xpath(
            '//*[@id="__EVENTVALIDATION"]/@value')[0]
        self.data["drxiaoqu"] = self.xiaoqu
        self.data.update(getDateData())

    def getSquaredPage(self):
        try:
            self.resp.append(httpx.post(
                self.url, data=self.data, cookies=self.cookies))
        except:
            self.result = self.errmsg
            return None
        self.doc.append(HTML(self.resp[1].text))

        self.data["__VIEWSTATE"] = self.doc[1].xpath(
            '//*[@id="__VIEWSTATE"]/@value')[0]
        self.data["__EVENTVALIDATION"] = self.doc[1].xpath(
            '//*[@id="__EVENTVALIDATION"]/@value')[0]
        self.data["drlou"] = self.louming
        self.data["txtRoomid"] = self.fangjian

    def getFinalResult(self):
        try:
            self.resp.append(httpx.post(
                self.url, data=self.data, cookies=self.cookies))
        except:
            self.result = self.errmsg
            return None
        self.doc.append(HTML(self.resp[2].text))
        try:
            self.finalResult = self.doc[2].xpath(
                '//*[@id="lableft"]/text()')[0]
            df = self.findPat("账户余额：.*元", 5, -1, float)
            du = self.findPat("剩余电量：.*度", 5, -1, float)
            result = {
                "账户余额": df,
                "剩余电量": du
            }
            return result
        except IndexError:
            result = {
                "账户余额": -1.0,
                "剩余电量": -1.0
            }
            return result


if __name__ == "__main__":
    a = Elec("04", "凌云四", "0203")
    print(a.getElec())
