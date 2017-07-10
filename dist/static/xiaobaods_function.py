#!usr/bin/env python3
#! -*- coding: gbk -*-
# SQL_msg
from dateutil.parser import parse
import numpy as np
import pymysql
import datetime
import pandas as pd
import configparser
import time
import sys,os
import codecs
# SQL msg
def conftodict(filename,path=""):
    #! -*- coding: utf8 -*-
    # 2017-04-11 添加脚本路径锁定
    # 2017-04-27 修补BUG，"/"
    if path=="":
        path = os.path.dirname(__file__)+"/"
    dic={}
    cp = configparser.SafeConfigParser()
    cp.read(path+filename)
    s = cp.sections()
    for i in s:
        dic[i]={}
        for j in cp.options(i):
            dic[i][j]=cp.get(i,j)
    return dic
SQL_msg = conftodict("xiaobaods_SQL.conf")
# Store Group
storegroup = {}
try:
    f = codecs.open('storegroup.txt','r','utf-8')
    storegrouptxt = f.readlines()
    for i in range(1,len(storegrouptxt)): # 第一行为编码行，略去
        storegroup[storegrouptxt[i].split(":")[0]]=storegrouptxt[i].split(":")[1].split("\r\n")[0].split(",")
    f.close()
except:
    pass
def storegrouplist():
    import json
    print(json.dumps([i for i in storegroup]))
# 将没有后缀的情况加入列表，避免误搜
stored = ["","官方旗舰店","旗舰店","服饰旗舰店","服饰专营店","专卖店"]
# Function
def xiaobaods_a(date="",category="牛仔裤",length=7,SQL="xiaobaods",table="bc_attribute_granularity_sales",variable="热销排名",fillna="",debug=0,path="",keyword="日期：",storechoice="",storegroupchoice=""):
    # 2017-04-11 添加keyword隐藏参数：'日期：'
    # 2017-04-12 修复可能引起数据库检索合并重复值的BUG
    # 2017-04-28 更新了MySQL检索索引和优化了查询函数，使得检索时间缩短为原来的3%，需对检索结果准确性进行观察认证
    # 2017-05-15 storechoice > storegroup choice参数,对结果进行筛选，后缀容错
    # 2017-06-03 fillna更新，添加bd
    time_s = time.time()
    latest_date=datetime.datetime.today().date()-datetime.timedelta(1)
    if category not in ["牛仔裤","打底裤","休闲裤"]:
        category="牛仔裤"
    if length>14 or length<3:
        length=7
    if SQL not in SQL_msg:
        SQL=SQL_msg[0]
    if table not in ["bc_attribute_granularity_sales","bc_attribute_granularity_visitor"]:
        table="bc_attribute_granularity_sales"
    if date=="":
        date = latest_date
    else:
        date=parse(date).date()  # 修改日期格式
    if table=="bc_attribute_granularity_sales":
        sql_select_f = "SELECT CT.`主图缩略图`,CT.`热销排名`,CT.`商品信息`,CT.`所属店铺`,CT.`支付子订单数`,CT.`交易增长幅度`,CT.`支付转化率指数`,CT.`宝贝链接`,CT.`店铺链接`,CT.`查看详情`,CT.`同款货源`"
        if variable not in ["热销排名","支付子订单数","交易增长幅度","支付转化率指数"]:
            variable="热销排名"
    elif table=="bc_attribute_granularity_visitor":
        sql_select_f = "SELECT CT.`主图缩略图`,CT.`热销排名`,CT.`商品信息`,CT.`所属店铺`,CT.`流量指数`,CT.`搜索人气`,CT.`支付子订单数`,CT.`宝贝链接`,CT.`店铺链接`,CT.`查看详情`,CT.`同款货源`"
        if variable not in ["热销排名","流量指数","搜索人气","支付子订单数"]:
            variable="热销排名"
    if storegroupchoice not in storegroup:
        storegroupchoice=""
    # Try to connect with the mysql and back a date which minimum.
    try:
        conn = pymysql.connect(host=SQL_msg[SQL]["host"], port=int(SQL_msg[SQL]["port"]), user=SQL_msg[SQL]["user"], passwd=SQL_msg[SQL]["passwd"], charset=SQL_msg[SQL]["charset"], db=SQL_msg[SQL]["db"])
        cursor = conn.cursor()
        cursor.execute("SELECT min(`日期`),max(`日期`) from "+table+" where `类目`='"+category+"';")
        date_limit = cursor.fetchall()
        date_floor = date_limit[0][0]
        date_ceiling = date_limit[0][1] 
        cursor.close()
        conn.close()
    except Exception as e:
        return e
    if date > latest_date:
        date = latest_date
    if date > date_ceiling:
        date = date_ceiling
    if date < date_floor + datetime.timedelta(length-1):
        date = date_floor + datetime.timedelta(length-1)
    # Main program.
    sql_select_m=""
    for i in range(length):
        sql_select_m += ",MAX(CASE ST.日期 WHEN "+str(date - datetime.timedelta(length-i-1)).replace("-","")+" THEN ST."+variable+" ELSE NULL END) AS `日期："+str(date - datetime.timedelta(length-i-1)).replace("-","")+"` "
    sql_select_e="FROM "+table+" AS CT LEFT JOIN "+table+" AS ST ON CT.`宝贝链接` = ST.`宝贝链接` WHERE CT.`日期` = "+str(date).replace("-","")+" AND CT.类目 = '"+category+"' AND ST.日期 >= "+str(date - datetime.timedelta(length)).replace("-","")+" AND ST.类目 = '"+category+"' GROUP BY CT.`热销排名`,CT.`"+variable+"` ORDER BY CT.`热销排名`;"
    # read msg from Mysql
    conn = pymysql.connect(host=SQL_msg[SQL]["host"], port=int(SQL_msg[SQL]["port"]), user=SQL_msg[SQL]["user"], passwd=SQL_msg[SQL]["passwd"], charset=SQL_msg[SQL]["charset"], db=SQL_msg[SQL]["db"])
    df = pd.io.sql.read_sql_query(sql_select_f+sql_select_m+sql_select_e,conn)
    conn.close()
    # storegroup
    if storechoice !="":
        storechoice = [storechoice+i for i in stored]
        df = df[df["所属店铺"].isin(storechoice)]
    elif storegroupchoice != "":
        df = df[df["所属店铺"].isin(storegroup[storegroupchoice])]
    if fillna == "bd":
        df = df.fillna(method="bfill",limit=1,axis=1)
        df.dropna(inplace=True)
    elif fillna == "drop":
        df.dropna(inplace=True)
    elif fillna =="":
        pass
    else:
        df = df.fillna(fillna)
    if debug not in [1,2,8,9]:
        print(df.to_json(orient="index"))
    elif debug== 8:
        return df
    elif debug== 2:
        print ("- Running time：%.4f s"%(time.time()-time_s))
        print("- date：%r \n- category：%r \n- length：%r \n- SQL：%r \n- table: %r \n- variable：%r \n- debug：%r \n- path: %r\n- keyword: %r\n- storechoice: %r\n- storegroupchoice: %r"%(str(date),category,str(length),SQL,table,variable,debug,path,keyword,storechoice,storegroupchoice))
    elif debug== 1:
        print ("- Running time：%.4f s"%(time.time()-time_s))
        print( "  SQL_choice: %r \n- category: %r \n- length: %r \n- date: %r \n- SQL: %r"%(SQL,category,str(length),str(date),sql_select_f+sql_select_m+sql_select_e))
    elif debug==9:
        import os
        print ("- Running time：%.4f s"%(time.time()-time_s))
        path_default=os.path.join(os.path.expanduser("~"), 'Desktop')
        if not os.path.isdir(path):
            path = path_default
        csv_filename="【数据组】["+table.split("_")[-1]+"_"+category+"_Top500"+"]"+variable+"_"+datetime.datetime.strftime(date,"%m%d")+"-"+str(length)+"_"+SQL+".csv"
        try:
            df.to_csv(path+"\\"+csv_filename)
            print("> 输出CSV文件：",path,",",csv_filename)
        except Exception as e:
            print("> 输出CSV文件失败，错误原因：",e)
def xiaobaods_w(date="",category="牛仔裤",length=7,SQL="xiaobaods",choice="热搜核心词",variable="排名",fillna="",debug=0,path="",keyword="日期："):
    # 2017-04-11 修补fillna的BUG，添加keyword隐藏参数：'日期:'
    # 2017-04-12 修复可能引起数据库检索合并重复值的BUG
    # 2017-04-13 Add dubug=7 Return paramter
    # 2017-06-03 fillna更新，添加bd
    time_s = time.time()
    latest_date=datetime.datetime.today().date()-datetime.timedelta(1)
    choice_list = {"热搜修饰词":{"table":"bc_searchwords_hotwords","variable":("搜索人气","相关搜索词数","点击率","点击人气","支付转化率","直通车参考价")},
                  "热搜品牌词":{"table":"bc_searchwords_hotwords","variable":("搜索人气","相关搜索词数","点击率","点击人气","支付转化率","直通车参考价")},
                  "热搜搜索词":{"table":"bc_searchwords_hotwords","variable":("搜索人气","商城点击占比","点击率","点击人气","支付转化率","直通车参考价")},
                  "热搜核心词":{"table":"bc_searchwords_hotwords","variable":("搜索人气","相关搜索词数","点击率","点击人气","支付转化率","直通车参考价")},
                  "热搜长尾词":{"table":"bc_searchwords_hotwords","variable":("搜索人气","商城点击占比","点击率","点击人气","支付转化率","直通车参考价")},
                  "飙升修饰词":{"table":"bc_searchwords_risewords",
                           "variable":("相关搜索词数","搜索人气","词均搜索增长幅度","点击人气","支付转化率","直通车参考价")},
                  "飙升品牌词":{"table":"bc_searchwords_risewords",
                           "variable":("相关搜索词数","搜索人气","词均搜索增长幅度","点击人气","支付转化率","直通车参考价")},
                  "飙升搜索词":{"table":"bc_searchwords_risewords",
                           "variable":("搜索增长幅度","搜索人气","点击率","点击人气","支付转化率","直通车参考价")},
                  "飙升核心词":{"table":"bc_searchwords_risewords",
                           "variable":("相关搜索词数","搜索人气","词均搜索增长幅度","点击人气","支付转化率","直通车参考价")},
                  "飙升长尾词":{"table":"bc_searchwords_risewords",
                           "variable":("搜索增长幅度","搜索人气","点击率","点击人气","支付转化率","直通车参考价")},}
    if category not in ["牛仔裤","打底裤","休闲裤"]:
        category="牛仔裤"
    if length>30 or length<3:
        length=7
    if SQL not in SQL_msg:
        SQL=SQL_msg[0]
    if choice not in choice_list:
        choice = "热搜修饰词"
    if variable not in choice_list[choice]["variable"]:
        variable="排名"
    if date=="":
        date = latest_date
    else:
        date=parse(date).date()  # 修改日期格式
    # Try to connect with the mysql and back a date which minimum.
    try:
        conn = pymysql.connect(host=SQL_msg[SQL]["host"], port=int(SQL_msg[SQL]["port"]), user=SQL_msg[SQL]["user"],passwd=SQL_msg[SQL]["passwd"],
                               charset=SQL_msg[SQL]["charset"], db=SQL_msg[SQL]["db"])
        cursor = conn.cursor()
        cursor.execute("SELECT min(`日期`),max(`日期`) from "+choice_list[choice]["table"]+" where `类目`='"+category+"' and `字段`='"+choice+"';")
        date_limit = cursor.fetchall()
        date_floor = date_limit[0][0]
        date_ceiling = date_limit[0][1] 
        cursor.close()
        conn.close()
    except Exception as e:
        return e
    if date > latest_date:
        date = latest_date
    if date > date_ceiling:
        date = date_ceiling
    if date < date_floor + datetime.timedelta(length-1):
        date = date_floor + datetime.timedelta(length-1)
    # Main program.
    sql_select_f="SELECT CT.`排名`,CT.`搜索词`"
    for i in range(len(choice_list[choice]["variable"])):
        sql_select_f += ",CT.`"+choice_list[choice]["variable"][i]+"`"
    sql_select_m=""
    for i in range(length):
        sql_select_m += ",MAX(CASE ST.日期 WHEN "+str(date - datetime.timedelta(length-i-1)).replace("-","")+" THEN ST."+variable+" ELSE NULL END) AS `"+keyword+str(date - datetime.timedelta(length-i-1)).replace("-","")+"` "
    sql_select_e="FROM "+choice_list[choice]["table"]+" AS CT LEFT JOIN "+choice_list[choice]["table"]+" AS ST ON CT.搜索词 = ST.搜索词 WHERE CT.`日期` = "+str(date).replace("-","")+" AND CT.类目 = '"+category+"' AND CT.字段='"+choice+"' AND ST.字段='"+choice+"' AND ST.日期 >= "+str(date - datetime.timedelta(length)).replace("-","")+" AND ST.类目 = '"+category+"' GROUP BY CT.`排名`,CT.`"+variable+"` ORDER BY CT.`排名`;"
    # Return parameter
    if debug == 7:
        return {"SQL_choice":SQL,"category":category,"length":str(length),"date":str(date),"SQL":sql_select_f+sql_select_m+sql_select_e,"choice":choice,"table":choice_list[choice]["table"],"variable":variable,"fillna":fillna,"debug":debug,"path":path}    
    # read msg from Mysql
    conn = pymysql.connect(host=SQL_msg[SQL]["host"], port=int(SQL_msg[SQL]["port"]), user=SQL_msg[SQL]["user"], passwd=SQL_msg[SQL]["passwd"], charset=SQL_msg[SQL]["charset"], db=SQL_msg[SQL]["db"])
    df = pd.io.sql.read_sql_query(sql_select_f+sql_select_m+sql_select_e,conn)
    conn.close()
    if fillna == "bd":
        df = df.fillna(method="bfill",limit=1,axis=1)
        df.dropna(inplace=True)
    elif fillna == "drop":
        df.dropna(inplace=True)
    elif fillna =="":
        pass
    else:
        df = df.fillna(fillna)
    # Debug
    if debug not in [1,2,8,9]:
        print(df.to_json(orient="index"))
    elif debug== 1:
        print ("- Running time：%.4f s"%(time.time()-time_s))
        print( "  SQL_choice: %r \n- category: %r \n- length: %r \n- date: %r \n- SQL: %r"%(SQL,category,str(length),str(date),sql_select_f+sql_select_m+sql_select_e))
    elif debug== 2:
        print ("- Running time：%.4f s"%(time.time()-time_s))
        print("- date：%r \n- category：%r \n- length：%r \n- SQL：%r \n- choice: %r \n- table: %r \n- variable：%r \n- fillna: %r \n- debug：%r \n- path: %r\n- keyword: %r"%(str(date),category,str(length),SQL,choice,choice_list[choice]["table"],variable,fillna,debug,path,keyword))
    elif debug== 8:
        return df
    elif debug== 9:
        import os
        print ("- Running time：%.4f s"%(time.time()-time_s))
        path_default=os.path.join(os.path.expanduser("~"), 'Desktop')
        if not os.path.isdir(path):
            path = path_default
        csv_filename="【数据组】["+choice_list[choice]["table"].split("_")[-1]+"_"+category+"_"+choice+"]"+variable+"_"+datetime.datetime.strftime(date,"%m%d")+"-"+str(length)+"_"+SQL+".csv"
        try:
            df.to_csv(path+"\\"+csv_filename)
            print("> 输出CSV文件：",path,",",csv_filename)
        except Exception as e:
            print("> 输出CSV文件失败，错误原因：",e)
def xiaobaods_ws(df_raw,df_sort,algorithm=1,alpha="",head=5,debug=0,path=""):
    # 2017-04-12 Algorithm EDT(Removed 06-03).
    # 2017-06-03 Rewrite Algorithm Log.
    if len(df_raw) > len(df_sort):
        df_raw = df_raw.ix[:len(df_sort),:]
    elif len(df_raw) < len(df_sort):
        df_sort = df_sort.ix[:len(df_raw),:]
    if head<3:
        head = 3
    elif head>len(df_raw):
        head = len(df_raw)
    if algorithm in [1,2]:
        # Log. Algorithm
        if alpha not in [2,"2","e",10,"10","1p"]:
            alpha = "10"
        def xlog(x):
            if alpha ==2 or alpha =="2":
                return np.log2(x)
            elif alpha=="e":
                return np.log(x)
            elif alpha=="1p":
                return np.log1p(x)
            else: # 10 or "10"
                return np.log10(x)
        df_sort['alg'] = (xlog(df_sort.iloc[:,12].tolist())+xlog(df_sort.iloc[:,13].tolist())+xlog(df_sort.iloc[:,14].tolist()))/3-(xlog(df_sort.iloc[:,8].tolist())+xlog(df_sort.iloc[:,9].tolist())+xlog(df_sort.iloc[:,10].tolist())+xlog(df_sort.iloc[:,11].tolist()))/4
        df_sort.sort_values(['alg'],inplace=True)
        df_raw = df_raw.loc[df_sort.index,:]
    else:
        head = len(df_raw)
    # Output
    if debug not in [1,2,8,9]:
        print(df_raw[:head].to_json(orient="index"))
    elif debug == 1:
        print("排序文档：\n",df_sort)
        return df_sort
    elif debug == 2:
        print("- df_raw：%r \n- df_sort：%r \n- algorithm：%r \n- alpha：%r \n- head：%r \n- debug：%r \n- List：%r \n"%(df_raw.shape,df_sort.shape,algorithm,alpha,head,debug,list(df_sort.index[:head])))
    elif debug == 8:
        return df_raw[:head]
    elif debug == 9:
        path_default=os.path.join(os.path.expanduser("~"), 'Desktop')
        if not os.path.isdir(path):
            path = path_default
        csv_filename="【数据组】排序算法输出数据文档.csv"
        try:
            df_raw[:head].to_csv(path+"\\"+csv_filename)
            print("> 输出CSV文件：",path,",",csv_filename)
        except Exception as e:
            print("> 输出CSV文件失败，错误原因：",e)
def xiaobaods_c(date="",category="牛仔裤",classification="款式",attributes="铅笔裤",length=7,SQL="xiaobaods",variable="热销排名",fillna="",debug=0,path="",keyword="日期：",storechoice="",storegroupchoice=""):
    # 2017-05-11 针对属性的查询模块
    # 2017-05-15 storechoice > storegroup choice参数,对结果进行筛选，后缀容错
    # 2017-06-03 fillna更新，添加bd
    time_s = time.time()
    latest_date=datetime.datetime.today().date()-datetime.timedelta(1)
    goal = {"打底裤":{"厚薄":['薄款','常规','加绒','加厚'],"裤长":['长裤','短裤','七分裤/九分裤']},"牛仔裤":{"款式":['哈伦裤','阔脚裤','铅笔裤','连衣裤','背带裤','直筒','灯笼裤','微喇裤','工装裤','垮裤'],"裤长":['长裤','超短裤','短裤','五分裤','九分裤','七分裤'],"腰型":['高腰','低腰','中腰'],"厚薄":['超薄','薄款','常规','加厚']}}
    if (category not in goal) or (classification not in goal[category]) or (attributes not in goal[category][classification]):
        category = "牛仔裤"
        classification="款式"
        attributes="铅笔裤"
    if length>14 or length<3:
        length=7
    if SQL not in SQL_msg:
        SQL=SQL_msg[0]
    table="bc_category_granularity"
    if date=="":
        date = latest_date
    else:
        date=parse(date).date()  # 修改日期格式
    if variable not in ["热销排名","支付子订单数","支付件数","支付转化率指数"]:
        variable="热销排名"
    if storegroupchoice not in storegroup:
        storegroupchoice=""
    # Try to connect with the mysql and back a date which minimum.
    try:
        conn = pymysql.connect(host=SQL_msg[SQL]["host"], port=int(SQL_msg[SQL]["port"]), user=SQL_msg[SQL]["user"], passwd=SQL_msg[SQL]["passwd"], charset=SQL_msg[SQL]["charset"], db=SQL_msg[SQL]["db"])
        cursor = conn.cursor()
        cursor.execute("SELECT min(`日期`),max(`日期`) from "+table+" where `类目`='"+category+"' and `类型`='"+classification+"' and `属性`='"+attributes+"';")
        date_limit = cursor.fetchall()
        date_floor = date_limit[0][0]
        date_ceiling = date_limit[0][1] 
        cursor.close()
        conn.close()
    except Exception as e:
        return e
    if date > latest_date:
        date = latest_date
    if date > date_ceiling:
        date = date_ceiling
    if date < date_floor + datetime.timedelta(length-1):
        date = date_floor + datetime.timedelta(length-1)
    # Main program.
    sql_select_f = "SELECT CT.`主图缩略图`,CT.`热销排名`,CT.`商品信息`,CT.`所属店铺`,CT.`支付子订单数`,CT.`支付件数`,CT.`支付转化率指数`,CT.`宝贝链接`,CT.`店铺链接`,CT.`查看详情`"
    sql_select_m=""
    for i in range(length):
        sql_select_m += ",MAX(CASE ST.日期 WHEN "+str(date - datetime.timedelta(length-i-1)).replace("-","")+" THEN ST."+variable+" ELSE NULL END) AS `日期："+str(date - datetime.timedelta(length-i-1)).replace("-","")+"` "
    sql_select_e="FROM "+table+" AS CT LEFT JOIN "+table+" AS ST ON CT.`宝贝链接` = ST.`宝贝链接` WHERE CT.`日期` = "+str(date).replace("-","")+" AND CT.类目 = '"+category+"' AND CT.类型 = '"+classification+"' AND CT.属性 = '"+attributes+"' AND ST.日期 >= "+str(date - datetime.timedelta(length)).replace("-","")+" AND ST.类目 = '"+category+"' AND CT.类型 = '"+classification+"' AND CT.属性 = '"+attributes+"' GROUP BY CT.`热销排名`,CT.`"+variable+"` ORDER BY CT.`热销排名`;"
    # read msg from Mysql
    conn = pymysql.connect(host=SQL_msg[SQL]["host"], port=int(SQL_msg[SQL]["port"]), user=SQL_msg[SQL]["user"], passwd=SQL_msg[SQL]["passwd"], charset=SQL_msg[SQL]["charset"], db=SQL_msg[SQL]["db"])
    df = pd.io.sql.read_sql_query(sql_select_f+sql_select_m+sql_select_e,conn)
    conn.close()
    # storegroup
    if storechoice !="":
        storechoice = [storechoice+i for i in stored]
        df = df[df["所属店铺"].isin(storechoice)]
    elif storegroupchoice != "":
        df = df[df["所属店铺"].isin(storegroup[storegroupchoice])]
    if fillna == "bd":
        df = df.fillna(method="bfill",limit=1,axis=1)
        df.dropna(inplace=True)
    elif fillna == "drop":
        df.dropna(inplace=True)
    elif fillna =="":
        pass
    else:
        df = df.fillna(fillna)
    if debug not in [1,2,8,9]:
        print(df.to_json(orient="index"))
    elif debug== 8:
        return df
    elif debug== 2:
        print ("- Running time：%.4f s"%(time.time()-time_s))
        print("- date：%r \n- category： %r\n- classification： %r\n- attributes：%r \n- length：%r \n- SQL：%r \n- table: %r \n- variable：%r \n- debug：%r \n- path: %r\n- keyword: %r\n- storechoice: %r\n- storegroupchoice: %r"%(str(date),category,classification,attributes,str(length),SQL,table,variable,debug,path,keyword,storechoice,storegroupchoice))
    elif debug== 1:
        print ("- Running time：%.4f s"%(time.time()-time_s))
        print( "  SQL_choice: %r \n- category: %r \n- length: %r \n- date: %r \n- SQL: %r"%(SQL,category,str(length),str(date),sql_select_f+sql_select_m+sql_select_e))
    elif debug==9:
        import os
        print ("- Running time：%.4f s"%(time.time()-time_s))
        path_default=os.path.join(os.path.expanduser("~"), 'Desktop')
        if not os.path.isdir(path):
            path = path_default
        csv_filename="【数据组】["+table.split("_")[1]+"_"+category+"_"+classification+"_"+attributes+"]"+variable+"_"+datetime.datetime.strftime(date,"%m%d")+"-"+str(length)+"_"+SQL+".csv"
        try:
            df.to_csv(path+"\\"+csv_filename)
            print("> 输出CSV文件：",path,",",csv_filename)
        except Exception as e:
            print("> 输出CSV文件失败，错误原因：",e)
def xiaobaods_m(date="",SQL="xiaobaods",category="牛仔裤",display="year",vs="onyear",variable="all",debug=0,path=""):
    '''
    # 2017-06-02 针对Panel的展示图形
    date default=''
    category default='牛仔裤','打底裤','休闲裤'
    display default='year','month','quarter','halfyear'
    vs default='onyear','sameperiod'
    variable default='all',element in columns
    debug default=0,1,2,8,9
    path default=""
    '''
    table = 'bc_industry_market'
    time_s = time.time()
    latest_date=datetime.datetime.today().date()-datetime.timedelta(1)
    if SQL not in SQL_msg:
        SQL=SQL_msg[0]
    if date =='':
        date = latest_date
    else:
        date=parse(date).date()  # 修改日期格式
    if category not in ['牛仔裤','打底裤','休闲裤']:
        category = '牛仔裤'
    if display not in ['year','month','quarter','halfyear']:
        display = 'year'
    if vs not in ['onyear','sameperiod']:
        vs = 'onyear'
    if variable not in ['all','访客数','收藏人数','收藏次数','浏览量','搜索点击率','搜索点击人数','加购次数','加购人数','客单价','浏览商品数','被浏览卖家数','卖家数','被支付卖家数','搜索人气','支付件数','交易指数','支付金额较父类目占比']:
        variable = 'all'
    display_time = {'year':365,'month':30,'quarter':90,'halfyear':180}
    if vs == 'onyear':
        cost_time = display_time[display]+365
    elif vs == 'sameperiod':
        cost_time = display_time[display]*2
    date_edge = date - datetime.timedelta(cost_time)  # 最小时间边界
    # Try to connect with the mysql and back a date which minimum.
    try:
        conn = pymysql.connect(host=SQL_msg[SQL]["host"], port=int(SQL_msg[SQL]["port"]), user=SQL_msg[SQL]["user"], passwd=SQL_msg[SQL]["passwd"], charset=SQL_msg[SQL]["charset"], db=SQL_msg[SQL]["db"])
        cursor = conn.cursor()
        cursor.execute("SELECT min(`日期`),max(`日期`) from "+table+" where `类目`='"+category+"';")
        date_limit = cursor.fetchall()
        date_floor = date_limit[0][0]
        date_ceiling = date_limit[0][1]
        cursor.close()
        conn.close()
    except Exception as e:
        return e
    if date > latest_date:
        date = latest_date
    if date > date_ceiling:
        date = date_ceiling
    if date_edge < date_floor:
        date = date_floor + datetime.timedelta(cost_time)
    # Main program.
    sql_select_1 = "SELECT * FROM "+table+" WHERE `类目`='"+ category +"' AND `日期` <='"+str(date)+"' AND `日期` >='"+ str(date-datetime.timedelta(display_time[display]-1))+"';"
    sql_select_0 = "SELECT * FROM "+table+" WHERE `类目`='"+ category +"' AND `日期` <='"+str(date - datetime.timedelta(cost_time) + datetime.timedelta(display_time[display]))+"' AND `日期` >='"+ str(date - datetime.timedelta(cost_time-1))+"';"
    conn = pymysql.connect(host=SQL_msg[SQL]["host"], port=int(SQL_msg[SQL]["port"]), user=SQL_msg[SQL]["user"], passwd=SQL_msg[SQL]["passwd"], charset=SQL_msg[SQL]["charset"], db=SQL_msg[SQL]["db"])
    df1 = pd.io.sql.read_sql_query(sql_select_1,conn)
    df0 = pd.io.sql.read_sql_query(sql_select_0,conn)
    conn.close()
    df = pd.merge(df1,df0.iloc[:,1:],left_index = True,right_index=True,suffixes=("_1","_0"))
    if debug not in [1,2,8,9]:
        print (df.to_json(orient="index"))
    elif debug == 1:
        print ("- Running time：%.4f s"%(time.time()-time_s))
        print( "  SQL_choice: %r \n- category: %r \n- date: %r \n- SQL_1: %r\n- SQL_0: %r"%(SQL,category,str(date),sql_select_1,sql_select_0))
    elif debug == 2:
        print ("- Running time：%.4f s"%(time.time()-time_s))
        print("- date：/%r/%r/ %r (%r ~[%r]~ %r) \n- times：[ %r ~ %r ] * [ %r ~ %r ] \n- category： %r\n- display： %r\n- vs：%r \n- variable：%r \n- table：%r \n- debug：%r \n- path: %r"%(str(date_edge),cost_time,str(date),str(date_floor),str(latest_date),str(date_ceiling),str(date - datetime.timedelta(cost_time-1)),str(date - datetime.timedelta(cost_time) + datetime.timedelta(display_time[display])),str(date-datetime.timedelta(display_time[display]-1)),str(date),category,display,vs,variable,table,debug,path))
    elif debug == 8:
        return df
    elif debug == 9:
        import os
        print ("- Running time：%.4f s"%(time.time()-time_s))
        path_default=os.path.join(os.path.expanduser("~"), 'Desktop')
        if not os.path.isdir(path):
            path = path_default
        csv_filename="【数据组】["+table+"_"+category+"_"+datetime.datetime.strftime(date,"%m%d")+"-"+display+"_"+vs+".csv"
        try:
            df.to_csv(path+"\\"+csv_filename)
            print("> 输出CSV文件：",path,",",csv_filename)
        except Exception as e:
            print("> 输出CSV文件失败，错误原因：",e)      