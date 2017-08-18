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
    # 2017-04-11 ��ӽű�·������
    # 2017-04-27 �޲�BUG��"/"
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
    for i in range(1,len(storegrouptxt)): # ��һ��Ϊ�����У���ȥ
        storegroup[storegrouptxt[i].split(":")[0]]=storegrouptxt[i].split(":")[1].split("\r\n")[0].split(",")
    f.close()
except:
    pass
def storegrouplist():
    import json
    print(json.dumps([i for i in storegroup]))
# ��û�к�׺����������б���������
stored = ["","�ٷ��콢��","�콢��","�����콢��","����רӪ��","ר����"]
# Function
def xiaobaods_a(date="",category="ţ�п�",length=7,SQL="xiaobaods",table="bc_attribute_granularity_sales",variable="��������",fillna="",debug=0,path="",keyword="���ڣ�",titlechoice="",storechoice="",storegroupchoice=""):
    # 2017-04-11 ���keyword���ز�����'���ڣ�'
    # 2017-04-12 �޸������������ݿ�����ϲ��ظ�ֵ��BUG
    # 2017-04-28 ������MySQL�����������Ż��˲�ѯ������ʹ�ü���ʱ������Ϊԭ����3%����Լ������׼ȷ�Խ��й۲���֤
    # 2017-05-15 storechoice > storegroup choice����,�Խ������ɸѡ����׺�ݴ�
    # 2017-06-03 fillna���£����bd
    # 2017-06-06 ��ӱ���ɸѡ���� titlechoice
    time_s = time.time()
    latest_date=datetime.datetime.today().date()-datetime.timedelta(1)
    if category not in ["ţ�п�","��׿�","���п�"]:
        category="ţ�п�"
    if length>14 or length<3:
        length=7
    if SQL not in SQL_msg:
        SQL=SQL_msg[0]
    if table not in ["bc_attribute_granularity_sales","bc_attribute_granularity_visitor"]:
        table="bc_attribute_granularity_sales"
    if date=="":
        date = latest_date
    else:
        date=parse(date).date()  # �޸����ڸ�ʽ
    if table=="bc_attribute_granularity_sales":
        sql_select_f = "SELECT CT.`��ͼ����ͼ`,CT.`��������`,CT.`��Ʒ��Ϣ`,CT.`��������`,CT.`֧���Ӷ�����`,CT.`������������`,CT.`֧��ת����ָ��`,CT.`��������`,CT.`��������`,CT.`�鿴����`,CT.`ͬ���Դ`"
        if variable not in ["��������","֧���Ӷ�����","������������","֧��ת����ָ��"]:
            variable="��������"
    elif table=="bc_attribute_granularity_visitor":
        sql_select_f = "SELECT CT.`��ͼ����ͼ`,CT.`��������`,CT.`��Ʒ��Ϣ`,CT.`��������`,CT.`����ָ��`,CT.`��������`,CT.`֧���Ӷ�����`,CT.`��������`,CT.`��������`,CT.`�鿴����`,CT.`ͬ���Դ`"
        if variable not in ["��������","����ָ��","��������","֧���Ӷ�����"]:
            variable="��������"
    if storegroupchoice not in storegroup:
        storegroupchoice=""
    # Try to connect with the mysql and back a date which minimum.
    try:
        conn = pymysql.connect(host=SQL_msg[SQL]["host"], port=int(SQL_msg[SQL]["port"]), user=SQL_msg[SQL]["user"], passwd=SQL_msg[SQL]["passwd"], charset=SQL_msg[SQL]["charset"], db=SQL_msg[SQL]["db"])
        cursor = conn.cursor()
        cursor.execute("SELECT min(`����`),max(`����`) from "+table+" where `��Ŀ`='"+category+"';")
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
        sql_select_m += ",MAX(CASE ST.���� WHEN "+str(date - datetime.timedelta(length-i-1)).replace("-","")+" THEN ST."+variable+" ELSE NULL END) AS `���ڣ�"+str(date - datetime.timedelta(length-i-1)).replace("-","")+"` "
    sql_select_e="FROM "+table+" AS CT LEFT JOIN "+table+" AS ST ON CT.`��������` = ST.`��������` WHERE CT.`����` = "+str(date).replace("-","")+" AND CT.��Ŀ = '"+category+"' AND ST.���� >= "+str(date - datetime.timedelta(length)).replace("-","")+" AND ST.��Ŀ = '"+category+"' GROUP BY CT.`��������`,CT.`"+variable+"` ORDER BY CT.`��������`;"
    # read msg from Mysql
    conn = pymysql.connect(host=SQL_msg[SQL]["host"], port=int(SQL_msg[SQL]["port"]), user=SQL_msg[SQL]["user"], passwd=SQL_msg[SQL]["passwd"], charset=SQL_msg[SQL]["charset"], db=SQL_msg[SQL]["db"])
    df = pd.io.sql.read_sql_query(sql_select_f+sql_select_m+sql_select_e,conn)
    conn.close()
    # titlechoice
    if titlechoice !="":
        df = df[[titlechoice in i for i in df["��Ʒ��Ϣ"]]]
    # storegroup
    if storechoice !="":
        storechoice = [storechoice+i for i in stored]
        df = df[df["��������"].isin(storechoice)] 
    elif storegroupchoice != "":
        df = df[df["��������"].isin(storegroup[storegroupchoice])]
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
        print ("- Running time��%.4f s"%(time.time()-time_s))
        print("- date��%r \n- category��%r \n- length��%r \n- SQL��%r \n- table: %r \n- variable��%r \n- debug��%r \n- path: %r\n- keyword: %r\n- storechoice: %r\n- storegroupchoice: %r"%(str(date),category,str(length),SQL,table,variable,debug,path,keyword,storechoice,storegroupchoice))
    elif debug== 1:
        print ("- Running time��%.4f s"%(time.time()-time_s))
        print( "  SQL_choice: %r \n- category: %r \n- length: %r \n- date: %r \n- SQL: %r"%(SQL,category,str(length),str(date),sql_select_f+sql_select_m+sql_select_e))
    elif debug==9:
        import os
        print ("- Running time��%.4f s"%(time.time()-time_s))
        path_default=os.path.join(os.path.expanduser("~"), 'Desktop')
        if not os.path.isdir(path):
            path = path_default
        csv_filename="�������顿["+table.split("_")[-1]+"_"+category+"_Top500"+"]"+variable+"_"+datetime.datetime.strftime(date,"%m%d")+"-"+str(length)+"_"+SQL+".csv"
        try:
            df.to_csv(path+"\\"+csv_filename)
            print("> ���CSV�ļ���",path,",",csv_filename)
        except Exception as e:
            print("> ���CSV�ļ�ʧ�ܣ�����ԭ��",e)
def xiaobaods_w(date="",category="ţ�п�",length=7,SQL="xiaobaods",choice="���Ѻ��Ĵ�",variable="����",fillna="",debug=0,path="",keyword="���ڣ�"):
    # 2017-04-11 �޲�fillna��BUG�����keyword���ز�����'����:'
    # 2017-04-12 �޸������������ݿ�����ϲ��ظ�ֵ��BUG
    # 2017-04-13 Add dubug=7 Return paramter
    # 2017-06-03 fillna���£����bd
    time_s = time.time()
    latest_date=datetime.datetime.today().date()-datetime.timedelta(1)
    choice_list = {"�������δ�":{"table":"bc_searchwords_hotwords","variable":("��������","�����������","�����","�������","֧��ת����","ֱͨ���ο���")},
                  "����Ʒ�ƴ�":{"table":"bc_searchwords_hotwords","variable":("��������","�����������","�����","�������","֧��ת����","ֱͨ���ο���")},
                  "����������":{"table":"bc_searchwords_hotwords","variable":("��������","�̳ǵ��ռ��","�����","�������","֧��ת����","ֱͨ���ο���")},
                  "���Ѻ��Ĵ�":{"table":"bc_searchwords_hotwords","variable":("��������","�����������","�����","�������","֧��ת����","ֱͨ���ο���")},
                  "���ѳ�β��":{"table":"bc_searchwords_hotwords","variable":("��������","�̳ǵ��ռ��","�����","�������","֧��ת����","ֱͨ���ο���")},
                  "������δ�":{"table":"bc_searchwords_risewords",
                           "variable":("�����������","��������","�ʾ�������������","�������","֧��ת����","ֱͨ���ο���")},
                  "���Ʒ�ƴ�":{"table":"bc_searchwords_risewords",
                           "variable":("�����������","��������","�ʾ�������������","�������","֧��ת����","ֱͨ���ο���")},
                  "���������":{"table":"bc_searchwords_risewords",
                           "variable":("������������","��������","�����","�������","֧��ת����","ֱͨ���ο���")},
                  "������Ĵ�":{"table":"bc_searchwords_risewords",
                           "variable":("�����������","��������","�ʾ�������������","�������","֧��ת����","ֱͨ���ο���")},
                  "�����β��":{"table":"bc_searchwords_risewords",
                           "variable":("������������","��������","�����","�������","֧��ת����","ֱͨ���ο���")},}
    if category not in ["ţ�п�","��׿�","���п�"]:
        category="ţ�п�"
    if length>30 or length<3:
        length=7
    if SQL not in SQL_msg:
        SQL=SQL_msg[0]
    if choice not in choice_list:
        choice = "�������δ�"
    if variable not in choice_list[choice]["variable"]:
        variable="����"
    if date=="":
        date = latest_date
    else:
        date=parse(date).date()  # �޸����ڸ�ʽ
    # Try to connect with the mysql and back a date which minimum.
    try:
        conn = pymysql.connect(host=SQL_msg[SQL]["host"], port=int(SQL_msg[SQL]["port"]), user=SQL_msg[SQL]["user"],passwd=SQL_msg[SQL]["passwd"],
                               charset=SQL_msg[SQL]["charset"], db=SQL_msg[SQL]["db"])
        cursor = conn.cursor()
        cursor.execute("SELECT min(`����`),max(`����`) from "+choice_list[choice]["table"]+" where `��Ŀ`='"+category+"' and `�ֶ�`='"+choice+"';")
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
    sql_select_f="SELECT CT.`����`,CT.`������`"
    for i in range(len(choice_list[choice]["variable"])):
        sql_select_f += ",CT.`"+choice_list[choice]["variable"][i]+"`"
    sql_select_m=""
    for i in range(length):
        sql_select_m += ",MAX(CASE ST.���� WHEN "+str(date - datetime.timedelta(length-i-1)).replace("-","")+" THEN ST."+variable+" ELSE NULL END) AS `"+keyword+str(date - datetime.timedelta(length-i-1)).replace("-","")+"` "
    sql_select_e="FROM "+choice_list[choice]["table"]+" AS CT LEFT JOIN "+choice_list[choice]["table"]+" AS ST ON CT.������ = ST.������ WHERE CT.`����` = "+str(date).replace("-","")+" AND CT.��Ŀ = '"+category+"' AND CT.�ֶ�='"+choice+"' AND ST.�ֶ�='"+choice+"' AND ST.���� >= "+str(date - datetime.timedelta(length)).replace("-","")+" AND ST.��Ŀ = '"+category+"' GROUP BY CT.`����`,CT.`"+variable+"` ORDER BY CT.`����`;"
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
        print ("- Running time��%.4f s"%(time.time()-time_s))
        print( "  SQL_choice: %r \n- category: %r \n- length: %r \n- date: %r \n- SQL: %r"%(SQL,category,str(length),str(date),sql_select_f+sql_select_m+sql_select_e))
    elif debug== 2:
        print ("- Running time��%.4f s"%(time.time()-time_s))
        print("- date��%r \n- category��%r \n- length��%r \n- SQL��%r \n- choice: %r \n- table: %r \n- variable��%r \n- fillna: %r \n- debug��%r \n- path: %r\n- keyword: %r"%(str(date),category,str(length),SQL,choice,choice_list[choice]["table"],variable,fillna,debug,path,keyword))
    elif debug== 8:
        return df
    elif debug== 9:
        import os
        print ("- Running time��%.4f s"%(time.time()-time_s))
        path_default=os.path.join(os.path.expanduser("~"), 'Desktop')
        if not os.path.isdir(path):
            path = path_default
        csv_filename="�������顿["+choice_list[choice]["table"].split("_")[-1]+"_"+category+"_"+choice+"]"+variable+"_"+datetime.datetime.strftime(date,"%m%d")+"-"+str(length)+"_"+SQL+".csv"
        try:
            df.to_csv(path+"\\"+csv_filename)
            print("> ���CSV�ļ���",path,",",csv_filename)
        except Exception as e:
            print("> ���CSV�ļ�ʧ�ܣ�����ԭ��",e)
def xiaobaods_ws(df_raw,df_sort,algorithm=1,alpha=[0.8,0.7,0.6,1.0,1.4,6,1000],head=10,debug=0,path=""):
    # 2017-04-12 Algorithm EDT(Removed 06-03).
    # 2017-06-03 Rewrite Algorithm Log.
    # 2017-06-08 Rewrite Ensamble Algorithm
    '''
    Ensamble Algorithm ������
    - Std Weight default = 0.8
    - Range Weight default = 0.7
    - Mean Gradient default = 1.0
    - Jump Gradient default = 0.8
    - Recent Gradient default = 1.2
    - Rank Weight(Square) default = 10
    - Plus default = 1000
    '''
    # �ַ�����ʽ��alpha����ת��
    try:
        alpha = [float(i) for i in alpha[1:-1].split(",")]
    except:
        pass
    if len(alpha) != 7:
        alpha = [0.8,0.7,0.6,1.0,1.4,6,1000]
    if len(df_raw) > len(df_sort):
        df_raw = df_raw.ix[:len(df_sort),:]
    elif len(df_raw) < len(df_sort):
        df_sort = df_sort.ix[:len(df_raw),:]
    if head<3:
        head = 3
    elif head>len(df_raw):
        head = len(df_raw)
    # Ensamble Algorithm
    df_sort['alg'] = (np.std(df_sort.iloc[:,8:],axis=1)*alpha[0]+(np.max(df_sort.iloc[:,8:],axis=1)-np.min(df_sort.iloc[:,8:],axis=1))*alpha[1]+(np.mean(df_sort.iloc[:,8:],axis=1)-df_sort.iloc[:,-1])*alpha[2]+(np.mean(df_sort.iloc[:,11:13],axis=1)-np.mean(df_sort.iloc[:,-2:],axis=1))*alpha[3]+(df_sort.iloc[:,-2]-df_sort.iloc[:,-1])*alpha[4])*(np.rint((-np.log2(df_sort.iloc[:,0].tolist())+10)**alpha[5]/((-np.log2(1)+10))**alpha[5]*alpha[6]*10)/10+1)*(np.sign(np.median(df_sort.iloc[:,8:],axis=1)-df_sort.iloc[:,12]))
    #df_sort['alg'] = (xlog(df_sort.iloc[:,12].tolist())+xlog(df_sort.iloc[:,13].tolist())+xlog(df_sort.iloc[:,14].tolist()))/3-(xlog(df_sort.iloc[:,8].tolist())+xlog(df_sort.iloc[:,9].tolist())+xlog(df_sort.iloc[:,10].tolist())+xlog(df_sort.iloc[:,11].tolist()))/4
    df_sort.sort_values(['alg'],inplace=True)
    df_raw = df_raw.loc[df_sort.index,:]
    # reset_index
    df_raw.reset_index(drop=True,inplace = True)
    # Output
    if debug not in [1,2,7,8,9]:
        print(df_raw[:head].to_json(orient="index"))
    elif debug == 1:
        print("�����ĵ���\n",df_sort)
        return df_sort
    elif debug == 2:
        print("- df_raw��%r \n- df_sort��%r \n- algorithm��%r \n- alpha��%r \n- head��%r \n- debug��%r \n- List��%r \n"%(df_raw.shape,df_sort.shape,algorithm,alpha,head,debug,list(df_sort.index[:head])))
    elif debug == 7:
        df_sort['0_std'] = (np.std(df_sort.iloc[:,8:15],axis=1))*alpha[0]
        df_sort['1_rgn'] = (np.max(df_sort.iloc[:,8:15],axis=1)-np.min(df_sort.iloc[:,8:15],axis=1))*alpha[1]
        df_sort['2_mg'] = (np.mean(df_sort.iloc[:,8:15],axis=1)-df_sort.iloc[:,14])*alpha[2]
        df_sort['3_jg'] = (np.mean(df_sort.iloc[:,11:13],axis=1)-np.mean(df_sort.iloc[:,13:15],axis=1))*alpha[3]
        df_sort['4_rg'] = (df_sort.iloc[:,13]-df_sort.iloc[:,14])*alpha[4]
        df_sort['0-4 sum'] = df_sort['0_std']+df_sort['1_rgn']+df_sort['2_mg']+df_sort['3_jg']+df_sort['4_rg']
        df_sort['5-6 pst'] = np.rint((-np.log2(df_sort.iloc[:,0].tolist())+10)**alpha[5]/((-np.log2(1)+10))**alpha[5]*alpha[6]*10)/10+1
        return df_sort
    elif debug == 8:
        return df_raw[:head]
    elif debug == 9:
        path_default=os.path.join(os.path.expanduser("~"), 'Desktop')
        if not os.path.isdir(path):
            path = path_default
        csv_filename="�������顿�����㷨��������ĵ�.csv"
        try:
            df_raw[:head].to_csv(path+"\\"+csv_filename)
            print("> ���CSV�ļ���",path,",",csv_filename)
        except Exception as e:
            print("> ���CSV�ļ�ʧ�ܣ�����ԭ��",e)
def xiaobaods_c(date="",category="ţ�п�",classification="��ʽ",attributes="Ǧ�ʿ�",length=7,SQL="xiaobaods",variable="��������",fillna="",debug=0,path="",keyword="���ڣ�",storechoice="",storegroupchoice=""):
    # 2017-05-11 ������ԵĲ�ѯģ��
    # 2017-05-15 storechoice > storegroup choice����,�Խ������ɸѡ����׺�ݴ�
    # 2017-06-03 fillna���£����bd
    time_s = time.time()
    latest_date=datetime.datetime.today().date()-datetime.timedelta(1)
    goal = {"��׿�":{"��":['����','����','����','�Ӻ�'],"�㳤":['����','�̿�','�߷ֿ�/�ŷֿ�']},"ţ�п�":{"��ʽ":['���׿�','���ſ�','Ǧ�ʿ�','���¿�','������','ֱͲ','������','΢����','��װ��','���'],"�㳤":['����','���̿�','�̿�','��ֿ�','�ŷֿ�','�߷ֿ�'],"����":['����','����','����'],"��":['����','����','����','�Ӻ�']}}
    if (category not in goal) or (classification not in goal[category]) or (attributes not in goal[category][classification]):
        category = "ţ�п�"
        classification="��ʽ"
        attributes="Ǧ�ʿ�"
    if length>14 or length<3:
        length=7
    if SQL not in SQL_msg:
        SQL=SQL_msg[0]
    table="bc_category_granularity"
    if date=="":
        date = latest_date
    else:
        date=parse(date).date()  # �޸����ڸ�ʽ
    if variable not in ["��������","֧���Ӷ�����","֧������","֧��ת����ָ��"]:
        variable="��������"
    if storegroupchoice not in storegroup:
        storegroupchoice=""
    # Try to connect with the mysql and back a date which minimum.
    try:
        conn = pymysql.connect(host=SQL_msg[SQL]["host"], port=int(SQL_msg[SQL]["port"]), user=SQL_msg[SQL]["user"], passwd=SQL_msg[SQL]["passwd"], charset=SQL_msg[SQL]["charset"], db=SQL_msg[SQL]["db"])
        cursor = conn.cursor()
        cursor.execute("SELECT min(`����`),max(`����`) from "+table+" where `��Ŀ`='"+category+"' and `����`='"+classification+"' and `����`='"+attributes+"';")
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
    sql_select_f = "SELECT CT.`��ͼ����ͼ`,CT.`��������`,CT.`��Ʒ��Ϣ`,CT.`��������`,CT.`֧���Ӷ�����`,CT.`֧������`,CT.`֧��ת����ָ��`,CT.`��������`,CT.`��������`,CT.`�鿴����`"
    sql_select_m=""
    for i in range(length):
        sql_select_m += ",MAX(CASE ST.���� WHEN "+str(date - datetime.timedelta(length-i-1)).replace("-","")+" THEN ST."+variable+" ELSE NULL END) AS `���ڣ�"+str(date - datetime.timedelta(length-i-1)).replace("-","")+"` "
    sql_select_e="FROM "+table+" AS CT LEFT JOIN "+table+" AS ST ON CT.`��������` = ST.`��������` WHERE CT.`����` = "+str(date).replace("-","")+" AND CT.��Ŀ = '"+category+"' AND CT.���� = '"+classification+"' AND CT.���� = '"+attributes+"' AND ST.���� >= "+str(date - datetime.timedelta(length)).replace("-","")+" AND ST.��Ŀ = '"+category+"' AND CT.���� = '"+classification+"' AND CT.���� = '"+attributes+"' GROUP BY CT.`��������`,CT.`"+variable+"` ORDER BY CT.`��������`;"
    # read msg from Mysql
    conn = pymysql.connect(host=SQL_msg[SQL]["host"], port=int(SQL_msg[SQL]["port"]), user=SQL_msg[SQL]["user"], passwd=SQL_msg[SQL]["passwd"], charset=SQL_msg[SQL]["charset"], db=SQL_msg[SQL]["db"])
    df = pd.io.sql.read_sql_query(sql_select_f+sql_select_m+sql_select_e,conn)
    conn.close()
    # storegroup
    if storechoice !="":
        storechoice = [storechoice+i for i in stored]
        df = df[df["��������"].isin(storechoice)]
    elif storegroupchoice != "":
        df = df[df["��������"].isin(storegroup[storegroupchoice])]
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
        print ("- Running time��%.4f s"%(time.time()-time_s))
        print("- date��%r \n- category�� %r\n- classification�� %r\n- attributes��%r \n- length��%r \n- SQL��%r \n- table: %r \n- variable��%r \n- debug��%r \n- path: %r\n- keyword: %r\n- storechoice: %r\n- storegroupchoice: %r"%(str(date),category,classification,attributes,str(length),SQL,table,variable,debug,path,keyword,storechoice,storegroupchoice))
    elif debug== 1:
        print ("- Running time��%.4f s"%(time.time()-time_s))
        print( "  SQL_choice: %r \n- category: %r \n- length: %r \n- date: %r \n- SQL: %r"%(SQL,category,str(length),str(date),sql_select_f+sql_select_m+sql_select_e))
    elif debug==9:
        import os
        print ("- Running time��%.4f s"%(time.time()-time_s))
        path_default=os.path.join(os.path.expanduser("~"), 'Desktop')
        if not os.path.isdir(path):
            path = path_default
        csv_filename="�������顿["+table.split("_")[1]+"_"+category+"_"+classification+"_"+attributes+"]"+variable+"_"+datetime.datetime.strftime(date,"%m%d")+"-"+str(length)+"_"+SQL+".csv"
        try:
            df.to_csv(path+"\\"+csv_filename)
            print("> ���CSV�ļ���",path,",",csv_filename)
        except Exception as e:
            print("> ���CSV�ļ�ʧ�ܣ�����ԭ��",e)
def xiaobaods_m(date="",SQL="xiaobaods",category="ţ�п�",display="year",vs="onyear",variable="all",debug=0,path=""):
    '''
    # 2017-06-02 ���Panel��չʾͼ��
    - date default=''
    - category default='ţ�п�','��׿�','���п�'
    - display default='year','month','quarter','halfyear'
    - vs default='onyear','sameperiod'
    - variable default='all',element in columns
    - debug default=0,1,2,8,9
    - path default=""
    '''
    table = 'bc_industry_market'
    time_s = time.time()
    latest_date=datetime.datetime.today().date()-datetime.timedelta(1)
    if SQL not in SQL_msg:
        SQL=SQL_msg[0]
    if date =='':
        date = latest_date
    else:
        date=parse(date).date()  # �޸����ڸ�ʽ
    if category not in ['ţ�п�','��׿�','���п�']:
        category = 'ţ�п�'
    if display not in ['year','month','quarter','halfyear']:
        display = 'year'
    if vs not in ['onyear','sameperiod']:
        vs = 'onyear'
    if variable not in ['all','�ÿ���','�ղ�����','�ղش���','�����','���������','�����������','�ӹ�����','�ӹ�����','�͵���','�����Ʒ��','�����������','������','��֧��������','��������','֧������','����ָ��','֧�����ϸ���Ŀռ��']:
        variable = 'all'
    display_time = {'year':365,'month':30,'quarter':90,'halfyear':180}
    if vs == 'onyear':
        cost_time = display_time[display]+365
    elif vs == 'sameperiod':
        cost_time = display_time[display]*2
    date_edge = date - datetime.timedelta(cost_time)  # ��Сʱ��߽�
    # Try to connect with the mysql and back a date which minimum.
    try:
        conn = pymysql.connect(host=SQL_msg[SQL]["host"], port=int(SQL_msg[SQL]["port"]), user=SQL_msg[SQL]["user"], passwd=SQL_msg[SQL]["passwd"], charset=SQL_msg[SQL]["charset"], db=SQL_msg[SQL]["db"])
        cursor = conn.cursor()
        cursor.execute("SELECT min(`����`),max(`����`) from "+table+" where `��Ŀ`='"+category+"';")
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
    sql_select_1 = "SELECT * FROM "+table+" WHERE `��Ŀ`='"+ category +"' AND `����` <='"+str(date)+"' AND `����` >='"+ str(date-datetime.timedelta(display_time[display]-1))+"';"
    sql_select_0 = "SELECT * FROM "+table+" WHERE `��Ŀ`='"+ category +"' AND `����` <='"+str(date - datetime.timedelta(cost_time) + datetime.timedelta(display_time[display]))+"' AND `����` >='"+ str(date - datetime.timedelta(cost_time-1))+"';"
    conn = pymysql.connect(host=SQL_msg[SQL]["host"], port=int(SQL_msg[SQL]["port"]), user=SQL_msg[SQL]["user"], passwd=SQL_msg[SQL]["passwd"], charset=SQL_msg[SQL]["charset"], db=SQL_msg[SQL]["db"])
    df1 = pd.io.sql.read_sql_query(sql_select_1,conn)
    df0 = pd.io.sql.read_sql_query(sql_select_0,conn)
    conn.close()
    df = pd.merge(df1,df0.iloc[:,1:],left_index = True,right_index=True,suffixes=("_1","_0"))
    if debug not in [1,2,8,9]:
        print (df.to_json(orient="index"))
    elif debug == 1:
        print ("- Running time��%.4f s"%(time.time()-time_s))
        print( "  SQL_choice: %r \n- category: %r \n- date: %r \n- SQL_1: %r\n- SQL_0: %r"%(SQL,category,str(date),sql_select_1,sql_select_0))
    elif debug == 2:
        print ("- Running time��%.4f s"%(time.time()-time_s))
        print("- date��/%r/%r/ %r (%r ~[%r]~ %r) \n- times��[ %r ~ %r ] * [ %r ~ %r ] \n- category�� %r\n- display�� %r\n- vs��%r \n- variable��%r \n- table��%r \n- debug��%r \n- path: %r"%(str(date_edge),cost_time,str(date),str(date_floor),str(latest_date),str(date_ceiling),str(date - datetime.timedelta(cost_time-1)),str(date - datetime.timedelta(cost_time) + datetime.timedelta(display_time[display])),str(date-datetime.timedelta(display_time[display]-1)),str(date),category,display,vs,variable,table,debug,path))
    elif debug == 8:
        return df
    elif debug == 9:
        import os
        print ("- Running time��%.4f s"%(time.time()-time_s))
        path_default=os.path.join(os.path.expanduser("~"), 'Desktop')
        if not os.path.isdir(path):
            path = path_default
        csv_filename="�������顿["+table+"_"+category+"_"+datetime.datetime.strftime(date,"%m%d")+"-"+display+"_"+vs+".csv"
        try:
            df.to_csv(path+"\\"+csv_filename)
            print("> ���CSV�ļ���",path,",",csv_filename)
        except Exception as e:
            print("> ���CSV�ļ�ʧ�ܣ�����ԭ��",e)
def xiaobaods_e(date="",SQL="xiaobaods",category="ţ�п�",attribute="����",variable="�ɽ���",debug=0,path=""):           
    '''
    # 2017-06-19 �����E�����ݵ�ƽ��չʾ
    - SQL ���ݿ���� "xiaobaods" or "Local"
    - category ��� "ţ�п�","���п�","��׿�","����ȹ","����Ůװ","�޿����޿�","��װ����װ��","����ȹ","�ɽ����ֲ�"������ҵ�ֲ����ݣ�
    - attribute ��Ӧ��������Ŀ *
    - variable ��ʾ���� "�ɽ���","���۶�","���ʱ�����","all"����ʾȫ����
    - debug ��ʾ���� 0,1,2,8,9
    - path ���·������debugΪ9ʱ��Ч
    '''
    table = 'shengejing_category'
    time_s = time.time()
    if date =='':
        date = datetime.date(2017,5,1)
    else:
        date=parse(date).date()  # �޸����ڸ�ʽ
    if date.day != 1:
        date = datetime.date(date.year,date.month,1)
    if date < datetime.date(2011,4,1):
        date = datetime.date(2011,4,1)
    if variable not in ["�ɽ���","���۶�","���ʱ�����","all"]:
        variable ="�ɽ���"
    if category not in ["ţ�п�","���п�","��׿�","����ȹ","����Ůװ","�޿����޿�","��װ����װ��","����ȹ","�ɽ����ֲ�"]:
        category ="ţ�п�"
    conn = pymysql.connect(host=SQL_msg[SQL]["host"], port=int(SQL_msg[SQL]["port"]), user=SQL_msg[SQL]["user"], passwd=SQL_msg[SQL]["passwd"], charset=SQL_msg[SQL]["charset"], db="baoersqlexternal")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT `����` from shengejing_category where `��Ŀ`='"+category+"' GROUP BY `����`;")
        attribute_tuple = cursor.fetchall()
        attribute_list = []
        for  i in range(len(attribute_tuple)):
            attribute_list.append(attribute_tuple[i][0])
    except Exception as e:
        print(e)
    if attribute=="list":
        print (pd.Series(attribute_list).to_json(orient="index"))
        return attribute_list
    elif attribute not in attribute_list:
        attribute = attribute_list[0]
    # Main Program.
    if variable != "all":
        sql_select = "select `����ֵ`,`"+variable+"` from shengejing_category where `��Ŀ`='"+category+"' and `����`='"+attribute+"' and `����`="+datetime.datetime.strftime(date,"%Y%m%d")+";"
    else:
        sql_select = "select `����ֵ`,`�ɽ���`,`���۶�`,`���ʱ�����` from shengejing_category where `��Ŀ`='"+category+"' and `����`='"+attribute+"' and `����`="+datetime.datetime.strftime(date,"%Y%m%d")+";"
    df = pd.io.sql.read_sql_query(sql_select,conn)
    conn.close()
    df.sort_values("�ɽ���",ascending=False,inplace=True)
    df.reset_index(drop=True,inplace=True)
    if debug not in [1,2,8,9]:
        print (df.to_json(orient="index"))
    elif debug == 1:
        print ("- Running time��%.4f s"%(time.time()-time_s))
        print( "  SQL: %r \n- category: %r \n- date: %r "%(sql_select,category,str(date)))
    elif debug == 2:
        print ("- Running time��%.4f s"%(time.time()-time_s))
        print("- date��%r \n- category�� %r\n- attribute�� %r\n- variable�� %r\n- debug: %r\n- path: %r"%(str(date),category,attribute,variable,debug,path))
    elif debug == 8:
        return df
    elif debug == 9:
        import os
        print ("- Running time��%.4f s"%(time.time()-time_s))
        path_default=os.path.join(os.path.expanduser("~"), 'Desktop')
        if not os.path.isdir(path):
            path = path_default
        csv_filename="�������顿["+table+"_"+category+"_"+attribute+"_"+variable+"_"+datetime.datetime.strftime(date,"%Y%m")+".csv"
        try:
            df.to_csv(path+"\\"+csv_filename)
            print("> ���CSV�ļ���",path,",",csv_filename)
        except Exception as e:
            print("> ���CSV�ļ�ʧ�ܣ�����ԭ��",e)
def xiaobaods_et(SQL="xiaobaods",category="ţ�п�",attribute="����",feature="",variable="all",stats=0,debug=0,path=""):
    '''
    # 2017-06-30 �����E�����ݵ�����ȡ��
    - SQL ���ݿ���� "xiaobaods" or "Local"
    - category ��� "ţ�п�","���п�","��׿�","����ȹ","����Ůװ","�޿����޿�","��װ����װ��","����ȹ","�ɽ����ֲ�"������ҵ�ֲ����ݣ�
    - attribute ��Ӧ��������Ŀ/"list" ����attribut�б�
    - feature ��Ӧ�����ڵ�����/"list" ����feature�б�/"sum"��"all" ���㵱ǰ�������������ĺ�
    - variable ��ʾ���� "�ɽ���","���۶�","���ʱ�����","all"����ʾȫ����
    - stats ͳ���� 0 Ϊ���任��1Ϊ�ٷֱȣ�
    - debug ��ʾ���� 0,1,2,8,9
    - path ���·������debugΪ9ʱ��Ч
    '''
    table = 'shengejing_category'
    time_s = time.time()
    if variable not in ["�ɽ���","���۶�","���ʱ�����","all"]:
        variable ="all"
    if category not in ["ţ�п�","���п�","��׿�","����ȹ","����Ůװ","�޿����޿�","��װ����װ��","����ȹ","�ɽ����ֲ�"]:
        category ="�ɽ����ֲ�"
    conn = pymysql.connect(host=SQL_msg[SQL]["host"], port=int(SQL_msg[SQL]["port"]), user=SQL_msg[SQL]["user"], passwd=SQL_msg[SQL]["passwd"], charset=SQL_msg[SQL]["charset"], db="baoersqlexternal")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT `����` from shengejing_category where `��Ŀ`='"+category+"' GROUP BY `����`;")
        attribute_tuple = cursor.fetchall()
        attribute_list = []
        for  i in range(len(attribute_tuple)):
            attribute_list.append(attribute_tuple[i][0])
    except Exception as e:
        print(e)
    if attribute=="list":
        print (pd.Series(attribute_list).to_json(orient="index"))
        return attribute_list
    elif attribute not in attribute_list:
        attribute = attribute_list[0]
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT `����ֵ` from shengejing_category where `��Ŀ`='"+category+"' and ����='"+attribute+"' GROUP BY `����ֵ`;")
        feature_tuple = cursor.fetchall()
        feature_list = []
        for  i in range(len(feature_tuple)):
            feature_list.append(feature_tuple[i][0])
    except Exception as e:
        print(e)
    if feature=="list":
        print (pd.Series(feature_list).to_json(orient="index"))
        return feature_list
    elif feature =="sum" or feature =="all":
        stats = 2
        feature = feature_list[0]
    elif feature not in feature_list:
        feature = feature_list[0]
    # Main Program.
    if stats !=2:
        if variable != "all":
            sql_select = "select `����`,`"+variable+"` from shengejing_category where `��Ŀ`='"+category+"' and `����`='"+attribute+"' and `����ֵ`='"+feature+"' ORDER BY `����`;"
        elif variable == "all": 
            sql_select = "select `����`,`�ɽ���`,`���۶�`,`���ʱ�����` from shengejing_category where `��Ŀ`='"+category+"' and `����`='"+attribute+"' and `����ֵ`='"+feature+"' ORDER BY `����`;"
    else:
        if variable != "all":
            sql_select = "select `����`,sum(`"+variable+"`) as "+variable+" from shengejing_category where `��Ŀ`='"+category+"' and `����`='"+attribute+"' GROUP BY `����` ORDER BY `����`;"
        elif variable == "all":
            sql_select = "select `����`,sum(`�ɽ���`) as `�ɽ���`,sum(`���۶�`) as `���۶�`,sum(`���ʱ�����`) as `���ʱ�����` from shengejing_category where `��Ŀ`='"+category+"' and `����`='"+attribute+"' GROUP BY `����` ORDER BY `����`;"
    df = pd.io.sql.read_sql_query(sql_select,conn)
    if variable != "all":
        sql_select_sum = "select `����`,sum(`"+variable+"`) as "+variable+" from shengejing_category where `��Ŀ`='"+category+"' and `����`='"+attribute+"' and `����`>="+datetime.datetime.strftime(df["����"].min(),'%Y%m%d')+" and `����`<="+datetime.datetime.strftime(df["����"].max(),'%Y%m%d')+" GROUP BY `����`,`����` ORDER BY `����`;"
    else:
        sql_select_sum = "select `����`,sum(`�ɽ���`) as `�ɽ���`,sum(`���۶�`) as `���۶�`,sum(`���ʱ�����`) as `���ʱ�����` from shengejing_category where `��Ŀ`='"+category+"' and `����`='"+attribute+"' and `����`>="+datetime.datetime.strftime(df["����"].min(),'%Y%m%d')+" and `����`<="+datetime.datetime.strftime(df["����"].max(),'%Y%m%d')+" GROUP BY `����`,`����` ORDER BY `����`;"
    df_sum = pd.io.sql.read_sql_query(sql_select_sum,conn)
    if stats==1:
        df = pd.concat([df.loc[:,"����"],df.iloc[:,1:]/df_sum.iloc[:,1:]],axis=1)
    if stats==2:
        df = df_sum
    conn.close()
    if debug not in [1,2,8,9]:
        print (df.to_json(orient="index"))
    elif debug == 1:
        print ("- Running time��%.4f s"%(time.time()-time_s))
        print( "  SQL: %r \n- SQL_sum: %r \n- category: %r \n- attribute: %r "%(sql_select,sql_select_sum,category,attribute))
    elif debug == 2:
        print ("- Running time��%.4f s"%(time.time()-time_s))
        print("- category�� %r\n- attribute�� %r\n- variable�� %r\n- debug: %r\n- path: %r\n- min_date��%r \n- max_date��%r \n- stats��%r"%(category,attribute,variable,debug,path,str(df["����"].min()),str(df["����"].max()),stats))
    elif debug == 8:
        return df
    elif debug == 9:
        import os
        print ("- Running time��%.4f s"%(time.time()-time_s))
        path_default=os.path.join(os.path.expanduser("~"), 'Desktop')
        if not os.path.isdir(path):
            path = path_default
        csv_filename="�������顿["+table+"_"+category+"_"+attribute+"_"+variable+"_"+feature+".csv"
        try:
            df.to_csv(path+"\\"+csv_filename)
            print("> ���CSV�ļ���",path,",",csv_filename)
        except Exception as e:
            print("> ���CSV�ļ�ʧ�ܣ�����ԭ��",e)