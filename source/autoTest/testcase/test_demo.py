import pytest
from pytest import mark, fixture


@fixture(scope="", params="", autouse="", ids="", name="")
def fixture1():
    print("this is fixture")


class TestSuite:
    num = 11

    # 使用setup_class为方法名时,该方法会在每个类之前执行
    def setup_class(self):
        print("class start")

    # 使用teardown_class为方法名时,该方法会在每个类之后执行
    def teardown_class(self):
        print("class end")

    # 使用setup_method为方法名时,该方法会在每个用例之前执行
    def setup_method(self):
        print("method start")

    # 使用teardown_method为方法名时,该方法会在每个用例之后执行
    def teardown_method(self):
        print("method end")

    @mark.skipif(num > 10, reason="this is skip test")  # 满足条件时跳过
    def test_01(self):
        print('this is test01')

    @mark.g2
    def test_02_solder(self):
        print('this is test01')

    @mark.run(order=2)
    @mark.g1
    def test_03_king(self):
        print('this is test04')

    @mark.run(order=1)
    @mark.g1
    @mark.skip(reason="this is skip test")  # 无条件跳过
    def test_04_queen(self):
        print('this is test04')
