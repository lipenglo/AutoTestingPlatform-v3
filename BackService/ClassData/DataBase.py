import MySQLdb

# Create reference here.
from ClassData.Logger import Logging as cls_Logging
from ClassData.Common import Common as cls_Common


# Create info here.

class DataBase(cls_Logging, cls_Common):
    # 连接测试
    def connect_test(self, dbType, dataBaseIp, port, userName, passWord):
        results = {}
        if dbType == "MySql":
            results = self.connect_mysql(dataBaseIp, port, userName, passWord)
        return results

    # 执行SQL
    def execute_sql(self, dbType, executeType, ip, port, user, pwd, dbName, sql):
        results = {}
        if dbType == 'MySql':
            results = self.execute_mysql(executeType, ip, port, user, pwd, dbName, sql)
        return results

    # 连接 Mysql
    def connect_mysql(self, ip, port, user, pwd):
        results = {}
        dataBaseList = []
        try:
            conn = MySQLdb.connect(
                host=ip,
                port=int(port),
                user=user,
                passwd=pwd,
                charset='utf8'
            )
            cur = conn.cursor()
            cur.execute('show databases')
            for i in range(cur.rowcount):
                row = cur.fetchone()
                dataBaseList.append(row[0])
            cur.close()
            conn.close()
        except BaseException as e:
            errorMsg = f"MySql连接失败:{e}"
            results['state'] = False
            results['errorMsg'] = errorMsg
            cls_Logging.print_log(self, 'error', 'connect_mysql', errorMsg)
        else:
            results['state'] = True
            results['dataBaseList'] = dataBaseList
        return results

    # 执行 mysql
    def execute_mysql(self, executeType, ip, port, user, pwd, dbName, sql):
        results = {}
        conn = MySQLdb.connect(host=ip, port=int(port), user=user, passwd=pwd, db=dbName, charset='utf8')
        try:
            cur = conn.cursor()
        except BaseException as e:
            errorMsg = f"MySql连接失败:{e}"
            results['state'] = False
            results['errorMsg'] = errorMsg
            cls_Logging.print_log(self, 'error', 'execute_mysql', errorMsg)
        else:
            try:
                res = cur.execute(sql)  # 执行SQL语句
                if executeType.lower() == "select":
                    resultsData = cur.fetchall()
                elif executeType.lower() in ["update", "delete"]:
                    conn.commit()
                    resultsData = f"受影响的行数:{res}"
                else:
                    raise ValueError('使用了未录入的Sql执行类型!')
            except BaseException as e:
                conn.rollback()  # 发生错误时回滚
                errorMsg = f"MySql执行失败:{e}"
                results['state'] = False
                results['errorMsg'] = errorMsg
                cls_Logging.print_log(self, 'error', 'execute_mysql', errorMsg)
            else:
                cur.close()
                conn.close()
                results['state'] = True
                results['resultsData'] = resultsData
        return results
