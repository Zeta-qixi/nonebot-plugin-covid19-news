from typing import Dict, Union, List
from .data import CITY_ID
import json
import requests


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

def policy_out(id: Union[str, int]) -> str:
    '''
    出行政策
    '''
    data = citypolicy_info(id)
    return  f"出行({data['leave_policy_date']})\n{data['leave_policy']}"

def policy_in(id: Union[str, int]) -> str:
    '''
    进入政策
    '''
    data = citypolicy_info(id)
    return f"进入({data['back_policy_date']})\n{data['back_policy']}"


def get_policy(out_id: Union[str, int], in_id: Union[str, int]=None) -> List[str]:

    '''
    input: 
        out_id 离开城市id 
        in_id: 进入城市id


    -> 进出政策
    '''
    if not in_id:
        in_id = out_id
    return([policy_out(out_id), policy_in(in_id)])



def get_city_poi_list(id: Union[str, int]) -> str:

    '''
    input: 城市id

    -> 地方 风险区域
    '''

    data = citypolicy_info(id)['poi_list']
    t = {'0':'🟢低风险','1':'🟡中风险', '2':'🔴高风险'}   
    list_ = [f"{t[i['type']]} {i['area'].split(i['city'])[-1]}" for i in data]
    return '\n\n'.join(list_) if data else "🟢全部低风险"

