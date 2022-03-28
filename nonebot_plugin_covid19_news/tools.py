import requests
from typing import Dict, List
import json
from .policy import POLICY_ID, get_city_poi_list, get_policy

class Area():
    def __init__(self, data):
        self.name = data['name']
        self.today = data['today']
        self.total = data['total']
        self.grade = data['total'].get('grade', '风险未确认')
        self.wzz_add = data['today'].get('wzz_add', 0)

        self.all_add = self.today['confirm'] + self.wzz_add
        self.children = data.get('children', None)

    @property
    def policy(self):
        return get_policy(POLICY_ID.get(self.name))

    @property
    def poi_list(self):
        return get_city_poi_list(POLICY_ID.get(self.name))

    @property
    def main_info(self):
        return (f"{self.name}({self.grade})\n新增确诊: {self.today['confirm']}\n新增无症状: {self.wzz_add}\n目前确诊: {self.total['nowConfirm']}")



class AreaList(Dict):
    def add(self, data):
        self[data.name] = data

    
class NewsData:
    def __init__(self):
        self.data = {}
        self.time = ''
        self.update_data()

    def update_data(self):
        url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
        res = requests.get(url).json()

        assert res['ret'] == 0
        data = json.loads(res['data'])

        if data['lastUpdateTime'] != self.time:
            
            self.time = data['lastUpdateTime']
            self.data = AreaList()

            def get_Data(data):
                
                if isinstance(data, list):
                    for i in data:
                        get_Data(i)

                if isinstance(data, dict):
                    area_ = data.get('children')
                    if area_:
                        get_Data(area_)

                    self.data.add(Area(data))

            get_Data(data['areaTree'][0])
            return True


