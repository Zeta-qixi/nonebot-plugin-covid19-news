from typing import Dict, Union
import json
import requests

POLICY_ID: Dict[str, Union[str, int]] = dict()


'''
    获取城市id 保存到 POLICY_ID
'''
url_city_list = 'https://r.inews.qq.com/api/trackmap/citylist?'
resp = requests.get(url_city_list)
res = resp.json()

for province in res['result']:
    citys = province.get('list')
    if citys:
        for city in citys:
            id = city['id']
            name = city['name']
            POLICY_ID[name] = id


def citypolicy_info(id: Union[str, int]) -> Dict:

    '''
    input: 城市id
     
     -> 地方疫情相关政策
    '''

    url_get_policy = f"https://r.inews.qq.com/api/trackmap/citypolicy?&city_id={id}"
    resp = requests.get(url_get_policy)
    res_ = resp.json()
    assert res_['message'] == 'success'
    return (res_['result']['data'][0])


def get_policy(id: Union[str, int]) -> str:

    '''
    input: 城市id

    -> 进出政策
    '''

    data = citypolicy_info(id)    
    msg = f"出行({data['leave_policy_date']})\n{data['leave_policy']}\n\
------\n\
进入({data['back_policy_date']})\n{data['back_policy']}"
    return (msg)


def get_city_poi_list(id: Union[str, int]) -> str:

    '''
    input: 城市id

    -> 地方 风险区域
    '''

    data = citypolicy_info(id)['poi_list']
    t = {'0':'🟢低风险','1':'🟡中风险', '2':'🔴高风险'}   
    list_ = [f"{t[i['type']]} {i['area'].split(i['city'])[-1]}" for i in data]
    return '\n\n'.join(list_) if data else "🟢全部低风险"

