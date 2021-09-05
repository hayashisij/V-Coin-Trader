from lib.private import PrivateApi


def test_get_permission():
    private_api = PrivateApi()

    hoge = private_api.get_permissions()
    assert hoge["status_code"] == 200
    print(hoge["response"])
