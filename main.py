import urllib3
import bs4
HTTP = urllib3.PoolManager()
account="帳號"
passwd="密碼"
keyword="你想報名的活動"
login_page=HTTP.request("POST","https://portalx.yzu.edu.tw/PortalSocialVB/Login.aspx")
VE=bs4.BeautifulSoup(login_page.data.decode(),'html.parser').select("#__VIEWSTATE")[0].get("value")
VR=bs4.BeautifulSoup(login_page.data.decode(),'html.parser').select("#__VIEWSTATEGENERATOR")[0].get("value")
EN=bs4.BeautifulSoup(login_page.data.decode(),'html.parser').select("#__EVENTVALIDATION")[0].get("value")
login_page=HTTP.request("POST",
             "https://portalx.yzu.edu.tw/PortalSocialVB/Login.aspx",
              fields={
                  "__VIEWSTATE":VE,
                  "__VIEWSTATEGENERATOR":VR,
                  "__EVENTVALIDATION":EN,
                  "Txt_UserID":account,
                  "Txt_Password":passwd,
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
    if str(bs4.BeautifulSoup(index,'html.parser').select("#divActivityDetail")).find(keyword) > 0 :
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
