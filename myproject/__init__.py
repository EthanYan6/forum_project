from pymysql import install_as_MySQLdb


# 让Django的ORM能以mysqldb的方式来调用PyMySQL
install_as_MySQLdb()