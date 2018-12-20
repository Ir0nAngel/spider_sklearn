import pymysql


class MysqlUtil:
    # 数据库连接
    conn = ''

    def __init__(self, host, user, password, DB):
        # 打开数据库连接
        self.conn = pymysql.connect(host, user, password, DB)

    def __del__(self):
        # 断开数据库连接
        self.conn.close()

    def insert_func(self, func_name, func_package):
        # 使用cursor()方法获取操作游标
        cursor = self.conn.cursor()
        # SQL 插入语句
        sql = "INSERT INTO config_scikitlearn_func (func_name, func_package, is_regresss, is_show, node_id, n_input, n_output) VALUES (%s, %s, 1, 1, 30, 1, 1)"
        try:
            # 执行sql语句
            cursor.execute(sql, (func_name, func_package))
            # 提交到数据库执行
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(e)
            # 如果发生错误则回滚
            self.conn.rollback()
            return 'error'

    def insert_arg(self, arg_name, sklearn_func_id, arg_value, is_optional, arg_doc):
        # 使用cursor()方法获取操作游标
        cursor = self.conn.cursor()
        # SQL 插入语句
        sql = "INSERT INTO config_scikitlearn_arg (arg_name, arg_value, is_show, scikitlearn_func_id, is_optional, arg_doc) VALUES (%s, %s, 1, %s, %s, %s)"
        try:
            # 执行sql语句
            cursor.execute(sql, (arg_name, arg_value, sklearn_func_id, is_optional, arg_doc))
            # 提交到数据库执行
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(e)
            # 如果发生错误则回滚
            self.conn.rollback()
            return 'error'

    def format_arg(self, arg_type):
        args = '%' + arg_type + '%'
        arg_type = arg_type + ','
        cursor = self.conn.cursor()
        # sql = "UPDATE config_scikitlearn_arg SET arg_type = ''"
        # sql = "UPDATE config_scikitlearn_arg SET arg_type = CONCAT(arg_type, %s) WHERE arg_value LIKE %s"
        sql = "UPDATE config_scikitlearn_arg SET arg_type = CONCAT(arg_type, 'dict') WHERE arg_type=''"
        try:
            # 执行sql语句
            cursor.execute(sql)
            # cursor.execute(sql, (arg_type, args))
            # 提交到数据库执行
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(e)
            # 如果发生错误则回滚
            self.conn.rollback()
            return 'error'


# mysql_util = MysqlUtil('localhost', 'root', '1234', 'AI_config')
mysql_util = MysqlUtil('10.28.0.196', 'AI_admin', '#O2hs7lSjug5ePEY', 'AI_config')
types = ['object', 'func', 'float', 'dict', 'bool', 'int', 'str', 'array-like', 'shape', 'size', 'RandomState', 'callable', 'None']
for type in types:
    mysql_util.format_arg(type)
# print(mysql_util.insert_func('hello'))
# print(mysql_util.insert_arg('zzz', 1, 'www', 'xxx'))
