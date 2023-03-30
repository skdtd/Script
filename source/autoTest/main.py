import pytest

if __name__ == '__main__':
    pytest.main([
        # '-s',  # 显示用例中的打印信息
        # '-v',  # 显示更详细的信息
        # '-q',  # 安静模式,不显示输出
        # '-x',  # 出现失败时直接退出
        # '-n 2',  # 开启2个线程运行测试
        # '-k king',  # 指定运行包含字符串的测试用例
        # '--capture=sys',
        # '--reruns=2',  # 失败时额外重试2次
        # '--maxfail=2',  # 失败两个用例时退出
        # "./testcase",  # 可以指定文件名或者目录或者用例的引用(./文件夹/文件名::类名::用例名)
        # '--clean-alluredir',
        # '--alluredir=allure-results',
        # '--html=report/report.html'  # 生成html报告

    ])
