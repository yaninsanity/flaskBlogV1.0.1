import os
import tempfile

import pytest
from myBlog import create_app
from myBlog.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    #创建并打开一个临时文件，
    #返回文件对象及其路径。该DATABASE路径被覆盖，使其指向这个临时路径，而不是实例文件夹。设置路径后，
    #将创建数据库表并插入测试数据。测试结束后，临时文件将被关闭并删除。
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        #告诉Flask应用程序处于测试模式。Flask更改了一些内部行为，
        #因此更容易测试，而其他扩展也可以使用该标志来更轻松地测试它们。
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
#该client固定电话 app.test_client()与所创建的应用程序对象app夹具。
#测试将使用客户端向应用程序发出请求而不运行服务器。
def client(app):
    return app.test_client()


#该runner夹具类似client。 app.test_cli_runner()创建一个可以调用应用程序注册的Click命令的运行器。

#Pytest通过将其函数名称与测试函数中的参数名称进行匹配来使用fixture。例如，test_hello 您接下来要编写的
#函数会带一个client参数。Pytest与clientfixture函数匹配，调用它，并将返回的值传递给测试函数。
@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)