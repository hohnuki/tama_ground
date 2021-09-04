from bs4 import BeautifulSoup
import time  # for sleep
from scraper import Scraper
from selenium import webdriver # installしたseleniumからwebdriverを呼び出せるようにする
from selenium.webdriver.common.keys import Keys # webdriverからスクレイピングで使用するキーを使えるようにする。

class GroundNotifier(Scraper) :

    def __init__(self):
      super(GroundNotifier, self).__init__()

    def convert_count_to_time(self, count) :
      ground_time = ""
      if (count == 4):
        ground_time = "8:00~"
      if (count == 8):
        ground_time = "10:00~"
      if (count == 12):
        ground_time = "12:00~"
      if (count == 16):
        ground_time = "14:00~"
      if (count == 20):
        ground_time = "16:00~"
      if (count == 24):
        ground_time = "18:00~"
      return ground_time

    def execute_main(self) :
      # TO_ADDRESS_1 = 'tk.cw.milds@gmail.com'
      TO_ADDRESS_2 = 'ohnukihiroki8585@yahoo.co.jp'
      SUBJECT = "多摩市のグラウンドに空きがあります"

      # 多摩市公共施設予約・案内システムのサイトを開く
      self.driver.get('https://www.google.com/search?q=%E5%A4%9A%E6%91%A9%E5%B8%82%E6%96%BD%E8%A8%AD%E4%BA%88%E7%B4%84%E3%83%88%E3%83%83%E3%83%97%E3%83%9A%E3%83%BC%E3%82%B8&rlz=1C5CHFA_enJP952JP953&sxsrf=ALeKk03nLyNGQ3GPujy3USUumboZdplVRg%3A1626688716370&ei=zEz1YMmFFvyT0PEP3926wA4&oq=%E5%A4%9A%E6%91%A9%E5%B8%82%E6%96%BD%E8%A8%AD%E4%BA%88%E7%B4%84t&gs_lcp=Cgdnd3Mtd2l6EAMYADIGCAAQBBAlOgcIIxCwAxAnOgUIABDNAkoECEEYAVDXLFiOMmCcO2gCcAB4AIABaIgBrgKSAQMxLjKYAQCgAQGqAQdnd3Mtd2l6yAEBwAEB&sclient=gws-wiz')
      self.click('#rso > div:nth-child(1) > div > div > div.yuRUbf > a > h3')
      # 詳細条件を指定するページに移動する
      self.click('#ykr00001c_YoyakuImgButton')
      self.click('#ykr30001c_MokutekiImgButton')
      time.sleep(1)
      self.click('#ykr30010 > div.panel-layout-aki.horizontal-block > div:nth-child(1) > div.content-substance.WidthPr90 > table > tbody > tr:nth-child(2) > td.table-cell-item.WidthPr50 > a')
      self.click('#ykr30011 > div.panel-layout-aki.horizontal-block > div:nth-child(1) > div.content-substance.WidthPr90 > table > tbody > tr:nth-child(16) > td.table-cell-item.WidthPr50 > a')
      time.sleep(1)
      self.click('#WeeklyAkiListCtrl_DayTypeCheckBoxList_1')
      self.click('#WeeklyAkiListCtrl_DayTypeCheckBoxList_2')
      self.click('#WeeklyAkiListCtrl_DayTypeCheckBoxList_3')
      self.click('#WeeklyAkiListCtrl_DayTypeCheckBoxList_4')
      self.click('#WeeklyAkiListCtrl_DayTypeCheckBoxList_5')
      self.click('#WeeklyAkiListCtrl_DayTypeCheckBoxList_6')
      self.click('#WeeklyAkiListCtrl_DayTypeCheckBoxList_7')
      self.click('#WeeklyAkiListCtrl_FilteringButton')
      self.click('#ykr31101 > div.panel-layout-aki.horizontal-block > div:nth-child(1) > table.table-calendar > tbody > tr:nth-child(1) > th:nth-child(3) > a')
      time.sleep(3)
      # ソースコードを取得
      html_main1 = self.driver.page_source
      # HTMLをパースする
      soup1 = BeautifulSoup(html_main1, 'lxml') # または、'html.parser'

      table_date1 = soup1.find(class_='label-datechange-currentdate calendar-selected-date')
      date1 = table_date1.get_text()

      south_col2 = []
      ippon_col = []
      south_availability2 = []
      ippon_availability = []
      south_colcount2 = 0
      ippon_colcount = 0
      south_availability = []
      message = ""

      for j in range(5):
        table_south = soup1.find_all(class_='calendar-datarow-day')[int(j)]
        south_catch = table_south.find_all('td')
        south_col = []
        south_availability = []
        south_count = 0

        for i in range(1,len(south_catch) ):
          south_catch = table_south.find_all('td')[int(i)]
          south_col.append(int(south_catch["colspan"]))
          south_availability.append(south_catch.get_text())
          south_count = 0

          for (ava,col) in zip(south_availability,south_col):
            if (south_count >= 4 and south_count <= 26 and str(ava) == "空き"):
              message += str(j) + date1 + "  " + self.convert_count_to_time(south_count) + "空きあり" + "\n"
              south_count += int(col)
            else:
              south_count += int(col)
              # print(south_count)


          print(str(ava) + ":" + str(col) + " total:" + str(south_count))

      # print(message)

      # for i in range(1,10):
      #   try:
      #     ippon_catch = table_ippon.find_all('td')[int(i)]
      #     ippon_col.append(int(ippon_catch["colspan"]))
      #     ippon_colcount += 1
      #   except IndexError as ie:
      #     break

      # for i in range(1,ippon_colcount+1):
      #   ippon_catch = table_ippon.find_all('td')[int(i)]
      #   ippon_availability.append(ippon_catch.get_text())

      # ippon_count = 0
      # for (ava,col) in zip(ippon_availability,ippon_col):
      #   if (ippon_count >= 4 and ippon_count <= 26 and str(ava) == "空き"):
      #     print("一本杉公園" + date1 + "  " + self.convert_count_to_time(ippon_count) + "空きあり")
      #   ippon_count += int(col)
      #   # print(str(ava) + ":" + str(col) + " total:" + str(ippon_count))

      # self.click('#DailyAkiListCtrl_NextWeekImgBtn')
      # time.sleep(2)
      # # ソースコードを取得
      # html_main2 = self.driver.page_source
      # # HTMLをパースする
      # soup2 = BeautifulSoup(html_main2, 'lxml') # または、'html.parser'
      # table_date2 = soup2.find(class_='label-datechange-currentdate calendar-selected-date')
      # date2 = table_date2.get_text()

      # table_south2 = soup2.find_all(class_='calendar-datarow-day')[0]
      # for i in range(1,10):
      #   try:
      #     south_catch2 = table_south2.find_all('td')[int(i)]
      #     south_col2.append(int(south_catch2["colspan"]))
      #     south_colcount2 += 1
      #   except IndexError as ie:
      #     break

      # for i in range(1,south_colcount2+1):
      #   south_catch2 = table_south2.find_all('td')[int(i)]
      #   south_availability2.append(south_catch2.get_text())

      # south_count2 = 0
      # for (ava,col) in zip(south_availability2,south_col2):
      #   if (south_count2 >= 4 and south_count2 <= 26 and str(ava) == "空き"):
      #     print("諏訪南公園" + date2 + "  " + self.convert_count_to_time(south_count2) + "空きあり")
      #   south_count2 += int(col)
      #   # print(str(ava) + ":" + str(col) + " total:" + str(south_count))

      # ブラウザを終了する
      self.driver.quit()



if __name__ == '__main__':
  notifier = GroundNotifier()
  notifier.execute_main()

