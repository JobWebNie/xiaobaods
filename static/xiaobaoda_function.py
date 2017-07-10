#!usr/bin/env python3
# -*- coding: gbk -*-
import sys,os
import xiaobaods_function as fc
import pandas as pd
import datetime
def analysis_ws(date="",length=15,SQL="xiaobaods",fillna="",head=5,algorithm=1):
    df = pd.DataFrame()
    for category in ["ţ�п�","��׿�","���п�"]:
        dic = {}
        for choice_list in ["�������δ�","����Ʒ�ƴ�","����������","���Ѻ��Ĵ�","���ѳ�β��"]:
            dic[choice_list]={}
            msg = list(fc.xiaobaods_ws(df_raw= fc.xiaobaods_w(date=date,length=length,SQL=SQL,debug=8,variable="����",fillna=fillna,category=category,choice=choice_list),
                    df_sort=fc.xiaobaods_w(date=date,length=length,SQL=SQL,fillna=500,variable="����",debug=8,category=category,choice=choice_list),
                    debug=8,algorithm=algorithm,head=head)["������"])
            for i in range(head):
                dic[choice_list][i] = msg[i]
        df1 = pd.DataFrame(dic).T
        df1["���"] = category
        try:
            df = pd.concat([df,df1])
        except:
            df = df1.copy()
    df.set_index(["���"],inplace=True,append=True)
    df.index = df.index.swaplevel()
    df.index.names = ["���","��"]
    df.columns = ["Top"+str(n+1) for n in range(head)]
    info = fc.xiaobaods_w(date=date,length=length,SQL=SQL,debug=7,variable="����",fillna=fillna,category=category,choice=choice_list)
    df.columns.names = [info["date"].replace("-","")[len(info["date"].split("-")[0]):]+"[:"+info["length"]+"]"]
    return df
def analysis_wl(date="",length=15,datelist=7,interval=1,SQL="xiaobaods",fillna="",head=5,algorithm=1,category="ţ�п�",choice="�������δ�"):
    df = pd.DataFrame()
    if category not in ["ţ�п�","��׿�","���п�"]:
        category = "ţ�п�"
    if choice not in ["�������δ�","����Ʒ�ƴ�","����������","���Ѻ��Ĵ�","���ѳ�β��"]:
        choice = "�������δ�"
    if datelist < 0:
        datelist = 7
    interval = int(interval)
    if interval < 0 or interval > 7:
        interval = 1
    dic = {}
    for i in range(datelist):
        date=datetime.datetime.strftime(datetime.datetime.today().date()-datetime.timedelta(1+i*interval),"%Y-%m-%d")
        dic[date] = {}
        msg = list(fc.xiaobaods_ws(df_raw= fc.xiaobaods_w(date=date,length=length,SQL=SQL,debug=8,fillna=fillna,category=category,choice=choice),
                    df_sort=fc.xiaobaods_w(date=date,length=length,SQL=SQL,fillna=500,variable="����",debug=8,category=category,choice=choice),
                    debug=8,algorithm=algorithm,head=head)["������"])
        for i in range(head):
            dic[date][i] = msg[i]
    df = pd.DataFrame(dic).T
    df.sort_index(inplace=True,ascending=True)
    df.columns = ["Top"+str(n+1) for n in range(head)]
    df.columns.names = [category+"["+choice+"]"]
    df.index.names = ["EDT.Sort"]
    return df.T