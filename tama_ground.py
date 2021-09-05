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
      if (count == 22):
        ground_time = "17:00~"
      if (count == 24):
        ground_time = "18:00~"
      if (count == 26):
        ground_time = "19:00~"
      return (ground_time)

    def park_name(self, nb) :
      ground_name = ""
      if (nb == 0):
        ground_name = "諏訪南公園"
      if (nb == 1):
        ground_name = "一本杉公園"
      if (nb == 2):
        ground_name = "貝取南公園"
      if (nb == 3):
        ground_name = "関戸公園"
      if (nb == 4):
        ground_name = "諏訪北公園"
      return (ground_name)


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
      time.sleep(2)
      # ソースコードを取得
      html_main_first = self.driver.page_source
      # HTMLをパースする
      soup_first = BeautifulSoup(html_main_first, 'lxml') # または、'html.parser'
      table_date_first = soup_first.find(class_='label-datechange-currentdate calendar-selected-date')
      date_first = table_date_first.get_text()

      message = ""
      for j in range(5):
        table_first = soup_first.find_all(class_='calendar-datarow-day')[int(j)]
        first_catch = table_first.find_all('td')
        first_col = []
        first_ava = []
        first_count = 0

        for i in range(1,len(first_catch) ):
          first_catch = table_first.find_all('td')[int(i)]
          first_col.append(int(first_catch["colspan"]))
          first_ava.append(first_catch.get_text())
          first_count = 0

        for (ava,col) in zip(first_ava,first_col):
          if (first_count >= 4 and first_count <= 26 and str(ava) == "空き"):
            message += str(self.park_name(j)) + date_first + "  " + self.convert_count_to_time(first_count) + "空きあり" + "\n"
          first_count += int(col)

      self.click('#DailyAkiListCtrl_NextDayImgBtn')
      time.sleep(2)
      html_main_second = self.driver.page_source
      soup_second = BeautifulSoup(html_main_second, 'lxml')
      table_date_second = soup_second.find(class_='label-datechange-currentdate calendar-selected-date')
      date_second = table_date_second.get_text()

      for j in range(5):
        table_second = soup_second.find_all(class_='calendar-datarow-day')[int(j)]
        second_catch = table_second.find_all('td')
        second_col = []
        second_ava = []
        second_count = 0

        for i in range(1,len(second_catch) ):
          second_catch = table_second.find_all('td')[int(i)]
          second_col.append(int(second_catch["colspan"]))
          second_ava.append(second_catch.get_text())
          second_count = 0

        for (ava,col) in zip(second_ava,second_col):
          if (second_count >= 4 and second_count <= 26 and str(ava) == "空き"):
            message += str(self.park_name(j)) + date_second + "  " + self.convert_count_to_time(second_count) + "空きあり" + "\n"
          second_count += int(col)
      print(message)


      # ブラウザを終了する
      self.driver.quit()



if __name__ == '__main__':
  notifier = GroundNotifier()
  notifier.execute_main()

