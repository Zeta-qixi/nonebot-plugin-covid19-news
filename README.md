# nonebot-plugin-covid19-news 😷
国内新冠消息查询

## 安装使用
### 方法一 使用nb-cli
```
nb plugin install nonebot_plugin_covid19_news
```

### 方法二 使用pip
```
# pip 下载包
pip install nonebot_plugin_covid19_news


# 配置 pyproject.toml

plugins = [
    ...,
    "nonebot_plugin_covid19_news",
    ]

```


## 主要功能

### 1. 疫情查询
指令: `地区 + 疫情`  
案例: `天津疫情`  
说明: 查询地区疫情信息（新增确诊 新增无症状 现有确诊）  
_补充: 可查询范围 全国、省级、市级地区疫情信息_

### 2. 疫情政策查询
指令: `地区 + 疫情政策`  
案例: `广州疫情政策`  
说明: 查询次数出行政策  
_补充: 出行政策只有市级，查询省级返回该地区所有市级行政区_

### 3. 垮城市政策查询
指令: `城市A + 到 + 城市B`  
案例: `广州到深圳`  
说明: 查询离开A市与进入B市的政策  
_补充:  疫情政策扩展功能，同只有市级_

### 4. 风险地区查询
指令: `城市 + 风险地区`  
案例: `长沙风险地区`  
说明: 长沙市内风险地区  
_补充: 只有市级，按高风险-低风险划分_

### 5. 关注地区疫情
指令: `关注疫情 + 地区`
案例: `关注疫情 北京`  
说明: 地区发生疫情时，推送疫情信息  
_补充: 每次数据更新时(30分钟)，如果该地区出现疫情，将在群聊或私信进行推送_

### 6. 取消关注地区疫情
指令: `取消关注疫情 + 地区` \ `取消疫情+地区` \ `取消推送疫情+地区`  
案例: `取消关注疫情  北京`  
说明: 取消关注疫情  



## 其他功能

### 异常新增警告
对国内新增异常的地区进行推送提醒  
需要修改配置文件`.env.dev`

### 图片发送
_疫情政策等出现长文本时可能发送失败，推荐使用图片发送_
1. 下载 `fonts/` 目录中字体 放到 `bot.py`同级目录的`data/fonts`中  
2. 配置`.env.dev`  添加以下一段
```
covid19_message_type = "image"
```



## 配置文件说明
```
// 异常新增警告
covid19 = {"notice":"True", "red-line": 1000, "filter":[],"group":[]}

    // 字段说明
    // notice: str                仅为 True 时开启功能
    // red-line: int              新增达到该数值会, 发送疫情信息
    // filter: List[str]          过滤城市/地区 （默认过滤 香港 台湾）
    // group: List[int] | str     发送到群; 为 all 时发送到所有群

// 消息发送类型（text, image）
covid19_message_type = "image"

```

## 更新log 📝
### 2022.2.14
添加取消推送功能

### 2022.2.15
添加风险地区查询功能功能

### 2022.3.23
无症状与确诊分开显示数据

### 2022.3.28
添加地区新增异常警告功能

### 2022.4.14
优化更新数据与推送的逻辑

### 2022.5.30
关注地区零新增不再推送（有无新增才是重点）

### 2022.6.20
出行政策以合并消息发送到群聊  （最近好忙 有些问题不能及时处理 见谅）

### 2022.7.31
图片方式发送信息 （默认发送文字 如需图片方式发送 需修改配置`.env.dev`）

### 2022.8.9
风险地区按等级排序发送

### 2022.8.27
群发消息风控提示 （建议设置图片发送）

### 2022.10.8
查询省级疫情政策与风险政策反馈省内市级地区疫情简讯

### 2022.11.10
更改数据源, 可以查询到现有确诊了

### 2022.11.28
全国疫情查询 `国内疫情`  `全国疫情`  
修改地区名不合法反馈

### 2022.12.01
修复同名地区查询冲突问题。市级、州级需要以`市` `州`结尾，如`吉林市疫情`

## 注意⚠️
数据更新、消息推送 目前以30分钟为周期  
本插件数据来自腾讯、百度等api, 数据存在一定滞后性; 真实数据请以国家卫健公布为准。
## TODO
- [x] 定时推送关注城市疫情信息 ⏰
- [x] 查询省份返回主要城市疫情信息 📍
- [ ] 一周内疫情变化图表 📈
- [x] 添加其他查询api 🔧
- [x] 图片形式发送
- [x] 同名地区问题 (吉林省 吉林市 / 海南省 海南州 ...) 


- 有想法欢迎提 issue 💡

