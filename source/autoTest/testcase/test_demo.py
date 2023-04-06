import random

from pytest import mark


class TestSuite:
    num = random.randint(0, 1)

    # 使用setup_class为方法名时,该方法会在每个类之前执行
    @staticmethod
    def setup_class():
        print("类前置")

    # 使用teardown_class为方法名时,该方法会在每个类之后执行
    @staticmethod
    def teardown_class():
        print("类后置")

    # 使用setup_method为方法名时,该方法会在每个用例之前执行
    @staticmethod
    def setup_method():
        print("方法前置")

    # 使用teardown_method为方法名时,该方法会在每个用例之后执行
    @staticmethod
    def teardown_method():
        print("方法后置")

    @mark.skipif(num == 1, reason="num等于1则跳过")  # 满足条件时跳过
    def test_01(self, fixture_for_func):
        print('this is test_01', TestSuite.num)

    # @mark.g2
    def test_02_solder(self, fixture_for_func):
        print('this is test_02_solder', fixture_for_func)

    @mark.run(order=2)
    # @mark.g1
    def test_03_king(self):
        print('this is test_03_king')

    @mark.run(order=1)
    # @mark.g1
    @mark.skip(reason="无条件跳过")  # 无条件跳过
    def test_04_queen(self):
        print('this is test_04_queen')
