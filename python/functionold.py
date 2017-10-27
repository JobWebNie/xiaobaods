#!/usr/bin/env python
# -*- coding: gbk -*-

"""
__title__ = ''
__author__ = 'Administrator'
__mtime__ = '2017-10-09'
"""
import time
import datetime
import pandas as pd
import pymysql
from dateutil.parser import parse


def xiaobaods_a(SQL_msg="", line_b=0, line_f=20, date="", category="ţ�п�", length=7, SQL="xiaobaods",
                table="bc_attribute_granularity_sales", variable="��������", fillna="", debug=0, path="", keyword="���ڣ�",
                rankl=0, rankm=0, titler="", storer="", v1l=0, v1m=0, v2l=0, v2m=0, v3l=0, v3m=0):
    '''
    # 2017-10-10 All rewrite
    '''
    if not SQL_msg:
        return None
    if line_b > line_f:
        line_b, line_f = line_f, line_b
    time_s = time.time()
    latest_date = datetime.datetime.today().date() - datetime.timedelta(1)
    if category not in ["ţ�п�", "��׿�", "���п�"]:
        category = "ţ�п�"
    if length > 14 or length < 3:
        length = 7
    if SQL not in SQL_msg:
        SQL = SQL_msg[0]
    if table not in ["bc_attribute_granularity_sales", "bc_attribute_granularity_visitor"]:
        table = "bc_attribute_granularity_sales"
    if date == "":
        date = latest_date
    else:
        date = parse(date).date()  # �޸����ڸ�ʽ
    if table == "bc_attribute_granularity_sales":
        sql_select_f = "SELECT CT.`��ͼ����ͼ`,CT.`��������`,CT.`��Ʒ��Ϣ`,CT.`��������`,CT.`֧���Ӷ�����`,CT.`������������`," \
                       "CT.`֧��ת����ָ��`,CT.`��������`,CT.`��������`,CT.`�鿴����`,CT.`ͬ���Դ`"
        if variable not in ["��������", "֧���Ӷ�����", "������������", "֧��ת����ָ��"]:
            variable = "��������"
    elif table == "bc_attribute_granularity_visitor":
        sql_select_f = "SELECT CT.`��ͼ����ͼ`,CT.`��������`,CT.`��Ʒ��Ϣ`,CT.`��������`,CT.`����ָ��`,CT.`��������`,CT." \
                       "`֧���Ӷ�����`,CT.`��������`,CT.`��������`,CT.`�鿴����`,CT.`ͬ���Դ`"
        if variable not in ["��������", "����ָ��", "��������", "֧���Ӷ�����"]:
            variable = "��������"
    # Try to connect with the mysql and back a date which minimum.
    try:
        conn = pymysql.connect(host=SQL_msg[SQL]["host"], port=int(SQL_msg[SQL]["port"]), user=SQL_msg[SQL]["user"],
                                passwd=SQL_msg[SQL]["passwd"], charset=SQL_msg[SQL]["charset"], db=SQL_msg[SQL]["db"])
        cursor = conn.cursor()
        cursor.execute("SELECT min(`����`),max(`����`) from " + table + " where `��Ŀ`='" + category + "';")
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
    if date < date_floor + datetime.timedelta (length - 1):
        date = date_floor + datetime.timedelta(length - 1)
    # Main program.
    sql_select_m = ""
    for i in range(length):
        sql_select_m += ",MAX(CASE ST.���� WHEN " + str(date - datetime.timedelta(length - i - 1)).replace("-",
                                        "") + " THEN ST." + variable + " ELSE NULL END) AS `���ڣ�" + str(
            date - datetime.timedelta(length - i - 1)).replace("-", "") + "` "
    sql_select_re = ""
    if 0 < rankl <= 500:
        sql_select_re += " AND CT.`��������`>=" + str(rankl)
    if 0 < rankm <= 500:
        sql_select_re += " AND CT.`��������`<=" + str(rankm)
    if titler:
        sql_select_re += " AND CT.`��Ʒ��Ϣ` REGEXP('" + titler + "')"
    if storer:
        sql_select_re += " AND CT.`��������` REGEXP('" + storer + "')"
    if v1l > 0:
        sql_select_re += " AND " + sql_select_f.split(",")[4] + "<=" + str(v1l)
    if v1m > 0:
        sql_select_re += " AND " + sql_select_f.split(",")[4] + ">=" + str(v1m)
    if v2l > 0:
        sql_select_re += " AND " + sql_select_f.split(",")[5] + "<=" + str(v2l)
    if v2m > 0:
        sql_select_re += " AND " + sql_select_f.split(",")[5] + ">=" + str(v2m)
    if v3l > 0:
        sql_select_re += " AND " + sql_select_f.split(",")[6] + "<=" + str(v3l)
    if v3m > 0:
        sql_select_re += " AND " + sql_select_f.split(",")[6] + ">=" + str(v3m)
    sql_select_b = "FROM " + table + " AS CT LEFT JOIN " + table + " AS ST ON CT.`��������` = ST.`��������` " \
                                                                   "WHERE CT.`����` = " + str(date).replace("-", "") \
            + " AND CT.��Ŀ = '" + category + "' AND ST.���� >= " + str(date - datetime.timedelta(length)).replace("-",
                                                     "") + " AND ST.��Ŀ = '" + category + "'" + sql_select_re
    sql_select_e = " GROUP BY CT.`��������`,CT.`" + variable + "` ORDER BY CT.`��������` LIMIT " + str(line_b) + ","\
                   + str(line_f-line_b) + ";"
    sql_select_c = "SELECT COUNT(*) AS total FROM " + table + " AS CT WHERE CT.`����` = " + str(date).replace("-", "") \
            + " AND CT.��Ŀ = '" + category + "'" + sql_select_re + ";"
    # read msg from Mysql
    conn = pymysql.connect(host=SQL_msg[SQL]["host"], port=int(SQL_msg[SQL]["port"]), user=SQL_msg[SQL]["user"],
                            passwd=SQL_msg[SQL]["passwd"], charset=SQL_msg[SQL]["charset"], db=SQL_msg[SQL]["db"])
    total = pd.read_sql_query(sql_select_c, conn).iloc[0, 0]
    df = pd.read_sql_query(sql_select_f + sql_select_m + sql_select_b + sql_select_e, conn)
    df["total"] = total
    conn.close()
    if fillna == "bd":
        df = df.fillna(method="bfill", limit=1, axis=1)
        df.dropna(inplace=True)
    elif fillna == "drop":
        df.dropna(inplace=True)
    elif fillna == "":
        pass
    else:
        df = df.fillna(fillna)
    if debug not in [1, 2, 8, 9]:
        print(df.to_json(orient="index"))
    elif debug == 8:
        return df
    elif debug == 2:
        print("- Running time��%.4f s" % (time.time() - time_s))
        print("- date��%r \n- category��%r \n- length��%r \n- page: (%r-%r) \n- SQL��%r \n- table: %r \n- variable��%r"
              " \n- debug��%r \n- path: %r\n- keyword: %r" % (str(date), category, str(length), line_f, line_b, SQL,
                                                          table, variable, debug, path, keyword))
    elif debug == 1:
        print("- Running time��%.4f s" % (time.time() - time_s))
        print("  SQL_choice: %r \n- category: %r \n- length: %r \n- date: %r \n- total_SQL: %r \n- SQL: %r" %
                (SQL, category, str(length), str(date), sql_select_c, sql_select_f + sql_select_m +
                 sql_select_b + sql_select_e))
    elif debug == 9:
        import os
        print("- Running time��%.4f s" % (time.time() - time_s))
        path_default = os.path.join(os.path.expanduser("~"), 'Desktop')
        if not os.path.isdir(path):
            path = path_default
        csv_filename = "�������顿[" + table.split("_")[
            -1] + "_" + category + "_Top500" + "]" + variable + "_" + datetime.datetime.strftime(date, "%m%d") + "-" \
                       + str(length) + "_" + SQL + ".csv"
        try:
            df.to_csv(path + "\\" + csv_filename)
            print("> ���CSV�ļ���", path, ",", csv_filename)
        except Exception as e:
            print("> ���CSV�ļ�ʧ�ܣ�����ԭ��", e)
