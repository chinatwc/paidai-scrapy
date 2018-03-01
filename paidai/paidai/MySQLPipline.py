import pymysql.cursors

class MySQLPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,  # 数据库端口
            db='paidai',  # 数据库名
            user='root',  # 数据库用户名
            passwd='root',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        self.cursor.execute(
            """insert into paidai(title,author,fav_nums,connent,time)
               value (%s, %s,%s,%s,%s)""",
            (item['title'],
             item['author'],
             item['fav_nums'],
             item['connent'],
             item['time'],))
        self.connect.commit()
        return item