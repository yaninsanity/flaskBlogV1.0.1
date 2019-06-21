import pytest
from flask import g, session
from myBlog.db import get_db


def test_register(client, app):
    #client.get()发出GET请求并返回ResponseFlask 返回的对象。同样， client.post()发出POST 请求，将datadict转换为表单数据。
    #要测试页面呈现成功，会发出一个简单的请求并检查a 。
    #如果渲染失败，Flask将返回一个 代码。200 OK status_code500 Internal Server Error
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    #headersLocation当注册视图重定向到登录视图时，将具有带登录URL 的标头。
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "select * from user where username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data




def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

    #client在with块中使用允许访问上下文变量，例如session在返回响应之后。
    #通常，session在请求之外访问会引发错误。测试logout与之相反login。注销后session不应包含user_id。


