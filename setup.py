#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
filepath = './README.md'
setup(
    name='nonebot-plugin-covid19-news',
    version='0.1.4',
    author='Zeta',
    author_email='',
    long_description=open(filepath, encoding='utf-8').read(),
    license="MIT Licence",
    url='https://github.com/Zeta-qixi/nonebot-plugin-covid19-news/',
    description='nonebot_plugin about covid-19 news',
    packages=['nonebot_plugin_covid19_news'],
    install_requires=[],

)