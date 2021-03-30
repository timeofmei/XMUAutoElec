import re
import httpx
from lxml import etree
from getDate import getDateData


class Elec:
    def __init__(self, xiaoqu, louming, fangjian):
        self.url = "http://elec.xmu.edu.cn/PdmlWebSetup/Pages/SMSMain.aspx"
        self.resp = []
        self.doc = []
        self.xiaoqu = xiaoqu
        self.louming = louming

        self.fangjian = fangjian
        self.data = {
            "dxdateStart_DDDWS": "0:0:-1:-10000:-10000:0:-10000:-10000:1",
            "dxdateStart_DDD_C_FNPWS": "0:0:-1:-10000:-10000:0:0px:-10000:1",
            "dxdateEnd_DDDWS": "0:0:-1:-10000:-10000:0:-10000:-10000:1",
            "dxdateEnd_DDD_C_FNPWS": "0:0:-1:-10000:-10000:0:0px:-10000:1"
        }

    def find(pattern, string, start=0, end=None, format=str):
        return format(re.compile(pattern).search(string).group()[start:end])

    def getElec(self):
        self.getInitPage()
        self.getSquaredPage()
        result = self.getFinalResult()
        return result

    def getInitPage(self):
        self.resp.append(httpx.get(self.url))
        self.doc.append(etree.HTML(self.resp[0].text))

        self.cookies = self.resp[0].cookies
        self.data["__VIEWSTATE"] = self.doc[0].xpath(
            '//*[@id="__VIEWSTATE"]/@value')[0]
        self.data["__EVENTVALIDATION"] = self.doc[0].xpath(
            '//*[@id="__EVENTVALIDATION"]/@value')[0]
        self.data["drxiaoqu"] = self.xiaoqu
        self.data.update(getDateData())

    def getSquaredPage(self):
        self.resp.append(httpx.post(
            self.url, data=self.data, cookies=self.cookies))
        self.doc.append(etree.HTML(self.resp[1].text))

        self.data["__VIEWSTATE"] = self.doc[1].xpath(
            '//*[@id="__VIEWSTATE"]/@value')[0]
        self.data["__EVENTVALIDATION"] = self.doc[1].xpath(
            '//*[@id="__EVENTVALIDATION"]/@value')[0]
        self.data["drlou"] = self.louming
        self.data["txtRoomid"] = self.fangjian

    def getFinalResult(self):
        self.resp.append(httpx.post(
            self.url, data=self.data, cookies=self.cookies))
        self.doc.append(etree.HTML(self.resp[2].text))
        try:
            finalResult = self.doc[2].xpath('//*[@id="lableft"]/text()')[0]
            df = self.find("账户余额：.*元", finalResult, 5, -1, float)
            du = self.find("剩余电量：.*度", finalResult, 5, -1, float)
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
