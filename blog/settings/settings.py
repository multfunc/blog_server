# Set the secret key to some random bytes.Keep this really secret!
SECRET_KEY = b'Lq\x94\xa3\x07\xb5\xe4U.,e7\xe46\x82S'
"""
生成session secret key
$ python -c 'import os; print(os.urandom(16))'
b'_5#y2L"F4Q8z\n\xec]/'
"""

DEBUG=True


#SQLAlchemy配置
DIALECT = 'mysql'
DRIVER = 'mysqlconnector'
USERNAME = 'root'
PASSWORD = '&*($%!Feng0'
HOST = '127.0.0.1'

PORT = '3306'
DATABASE = 'facebook_local'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False


