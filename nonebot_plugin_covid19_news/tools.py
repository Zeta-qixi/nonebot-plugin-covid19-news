import requests
from typing import Dict
import time
from datetime import datetime
import re


class Area():
    def __init__(self, data):

        def to_int(data):
            return int(data) if data else 0
     
        self.name = data['city'] if data.get('city') else data['area']
        self.confirmed_relative = to_int(data.get('confirmedRelative'))          # 新增确诊
        self.native_relative = to_int(data.get('nativeRelative'))                # 本土新增
        self.wzz_add = to_int(data.get('asymptomaticRelative'))                  # 新增无症状
        self.local_wzz_add = to_int(data.get('asymptomaticLocalRelative'))       # 新增本土无症状
        self.cur_confirm = to_int(data.get('curConfirm')  )                      # 现有确诊    
        self.all_add = self.confirmed_relative + self.wzz_add
        self.time = float(data.get('updateTime'))
        self.isUpdated = True
        if self.all_add == 0:
            self.isUpdated = False


    @property
    def update_time(self):
        return datetime.fromtimestamp(self.time).strftime('%Y-%m-%d %H:%M')

    @property
    def main_info(self):
        return (f"{self.name} {self.update_time}\n新增确诊: {self.confirmed_relative}\n新增无症状: {self.wzz_add}\n现有确诊: {self.cur_confirm}")

    def today_update(self):
        dt = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
        timeArray = time.strptime(dt, "%Y-%m-%d") # 0点时间戳
        return self.time >= time.mktime(timeArray)

    def __eq__(self, obj):
        return (isinstance(obj, Area) and self.all_add == obj.all_add)



class AreaList(Dict):
    def add(self, data):
        if self.get(data.name) != data:
            self[data.name] = data
            
    def get_data(self,name):
        if name[-1] in ['市', '省']:
            name = name[:-1]
        return self.get(name)

    
class NewsData:
    def __init__(self):
        self.data = AreaList()
        self.update_data()

    def update_data(self):
        url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner'
        response = requests.get(url)
        html_data = response.text
        json_str = re.findall('"component":\[(.*)\],', html_data)[0]
        null = None
        json_dict = eval(json_str)
        data = json_dict['caseList']

      
        for area in data:
            
            self.data.add(Area(area))
            for city in area.get("subList",[]):
                self.data.add(Area(city))


        return True


NewsBot = NewsData()