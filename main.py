import urllib3
import bs4
HTTP = urllib3.PoolManager()
login_page=HTTP.request("POST",
             "https://portalx.yzu.edu.tw/PortalSocialVB/Login.aspx",
              fields={
                  "__VIEWSTATE":"/wEPDwUKLTkyMDk2NTcxNA9kFgICAw9kFgQCAQ8WAh4JaW5uZXJodG1sBfICPGRpdiBzdHlsZT0nY29sb3I6IHJlZDsgZm9udC13ZWlnaHQ6IGJvbGQ7Jz7luLPomZ/ngrpzIOWKoOS4iuaCqOeahOWtuOiZn++8jOWmgnM5MjExMDE8L2Rpdj48ZGl2IHN0eWxlPSdjb2xvcjogcmVkOyBmb250LXdlaWdodDogYm9sZDsnPuWvhueivOeCuiDouqvku73oqLzlrZfomZ8o6Iux5paH5a2X6KuL5aSn5a+rKTwvZGl2PjxkaXYgc3R5bGU9J2NvbG9yOiBibGFjazsnPueZu+WFpeW+jOiri+WLmeW/heS/ruaUueaCqOeahOWvhueivDwvZGl2PjxiciAvPjxkaXYgc3R5bGU9J2NvbG9yOiBibGFjazsnPuW/mOiomOWvhueivO+8muiri+mAlea0veWcluabuOmkqOarg+WPsCjlgpnorYnku7Yp77yM5oiW6Zu75qCh5YWn5YiG5qmfMjMyMTwvZGl2PmQCAw9kFgZmD2QWAmYPZBYCZg8PFgQeCENzc0NsYXNzBQ5Mb2dpbkJhY2s4MDBfWR4EXyFTQgICZBYCZg9kFgJmD2QWAgIBDw8WBB8BBQ5Mb2dpbkJhY2syNzBfWR8CAgJkFgJmD2QWAmYPZBYKAgEPDxYCHgRUZXh0BQbluLPomZ9kZAIFDw8WAh8DBQblr4bnorxkZAIJDw8WBB4HVG9vbFRpcAUPRW5nbGlzaCBWZXJzaW9uHghJbWFnZVVybAUcLi9JbWFnZXMvSWNvbnMvVmVyc2lvblRXLnBuZxYCHgdvbmNsaWNrBRVDaGFuZ2VMYW5ndWFnZSgnVFcnKTtkAgsPDxYCHwMFBueZu+WFpWRkAg0PDxYCHwMFDioq5paw55Sf5rOo5oSPZGQCAQ9kFgJmDw8WBB8BBQ90YWJDZWxsTWlkZGxlX1kfAgICZBYEAgMPDxYEHwEFDnRhYmxlSG90UGFnZV9ZHwICAmQWAmYPZBYCZg9kFgJmDw8WAh8DBQznhrHploDlsIjpoIFkZAIFDw8WBB8BBRF0YWJsZUhvdFBhZ2VFbmRfWR8CAgJkZAIDD2QWAmYPZBYCZg8PFgQfAQUNTG9naW5Gb290ZXJfWR8CAgJkZGTyT2gnXdKy6dcClhG2S9KvWwKitQ==",
                  "__VIEWSTATEGENERATOR":"4F5352E6",
                  "__EVENTVALIDATION":"/wEdAAYZE+NrQEMnXQZ2m08gbZJj1vGYFjrtzIuId5C42O0AzRaVgZp528BwL4Heg6ju5IFPJEHWQZAV39IrTgU3OMCuz9Epgz+OXGhhMky+n/+RyLga9dtgamGDPrZlwtr3L501mImYpIoFcNzIUq9OwA27skCHhA==",
                  "Txt_UserID":'s+ID',
                  "Txt_Password":'passwd',
                  "ibnSubmit":"登入"
              })
portal_x_key = [i for i in login_page.headers["Set-Cookie"].split(", ") if i.find("ASP.NET") != -1][0].split(";")[0].split("=")[1]
Activitypage=HTTP.request("POST","https://portalx.yzu.edu.tw/PortalSocialVB/FMain/PageActivityAll.aspx", headers={"Cookie":"ASP.NET_SessionId="+portal_x_key}).data.decode("utf-8")
activitycode=[]
for i in bs4.BeautifulSoup(Activitypage,'html.parser').select("a"):
    if str(i).find("線上報名") > 0 :
        num=""
        for j in range(str(i).find("線上報名")-6,str(i).find("線上報名")-2) :num+=str(i)[j]
        activitycode.append(num)
for i in range(0,len(activitycode)) :
    index=HTTP.request("POST","https://portalx.yzu.edu.tw/PortalSocialVB/FPage/PageActivityDetail.aspx?Menu=Act&ActID="+activitycode[i],headers={"Cookie":"ASP.NET_SessionId="+portal_x_key,"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15"}).data.decode("utf-8")
    if str(bs4.BeautifulSoup(index,'html.parser').select("#divActivityDetail")).find("keyword") > 0 :
        print("https://portalx.yzu.edu.tw/PortalSocialVB/FPage/PageActivityDetail.aspx?Menu=Act&ActID="+activitycode[i])
        pos=str(bs4.BeautifulSoup(index,'html.parser').select("#divActivityDetail")).find("上限")+3
        up=""
        while str(bs4.BeautifulSoup(index,'html.parser').select("#divActivityDetail"))[pos+1].isdigit() :
            up+=str(bs4.BeautifulSoup(index,'html.parser').select("#divActivityDetail"))[pos]
            pos+=1
        up+=str(bs4.BeautifulSoup(index,'html.parser').select("#divActivityDetail"))[pos]
        pos=str(bs4.BeautifulSoup(index,'html.parser').select("#divActivityDetail")).find("已報名人數")+6
        now=""
        while str(bs4.BeautifulSoup(index,'html.parser').select("#divActivityDetail"))[pos+1].isdigit() :
            now+=str(bs4.BeautifulSoup(index,'html.parser').select("#divActivityDetail"))[pos]
            pos+=1
        now+=str(bs4.BeautifulSoup(index,'html.parser').select("#divActivityDetail"))[pos]
        print("總"+up+"\n已報"+now)
