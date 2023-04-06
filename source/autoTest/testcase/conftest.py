from pytest import fixture


@fixture(scope="function", autouse=True, params=["张三", "李四", "王五"], ids=["zhangsan", "lisi", "wangwu"])
def fixture_for_func(request):  # 变量名只能是request
    print("conftest 方法前置")
    yield request.param
    print("conftest 方法后置")


@fixture(scope="class", autouse=True)
def fixture_for_class():
    print("conftest 类前置")
    yield
    print("conftest 类后置")
