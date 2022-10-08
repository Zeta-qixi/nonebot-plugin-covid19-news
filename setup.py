#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
requirements = [r.strip() for r in open("requirements.txt", 'r', encoding='utf-8').readlines()]

setup(
    name='nonebot-plugin-covid19-news',
    version='0.6.0.1',
    author='Zeta',
    author_email='',
    long_description="https://github.com/Zeta-qixi/nonebot-plugin-covid19-news",
    license="MIT Licence",
    url='https://github.com/Zeta-qixi/nonebot-plugin-covid19-news/',
    description='nonebot_plugin about covid-19 news',
    packages=['nonebot_plugin_covid19_news'],
    install_requires=requirements,

)
