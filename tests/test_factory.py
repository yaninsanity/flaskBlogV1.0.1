from myBlog import create_app

#关于工厂本身的测试并不多。大多数代码都将针对每个测试执行，因此如果某些内容失败，其他测试将会注意到。

#唯一可以改变的行为是传递测试配置。如果未传递config，则应该有一些默认配置，否则应该重写配置。
def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'