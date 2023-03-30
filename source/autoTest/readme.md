# 安装RF

```bash
# 更新pip(py3.10)
python -m pip install --upgrade pip
# 安装rf和桌面端
pip install robotframework robotframework-ride robotframework-selenium2library robotframework-requests robotframework-appiumlibrary robotframework-databaselibrary  
# webdriver_manager
# robotframework-seleniumlibrary==3.0.0 open_browser关键字问题
```

# excel读取

```bash
pip install xToolkit 
```

# pytest

```bash
pip install -r requirements.txt
# main方法
# 使用allure生成报告, 将allure配置到环境
# https://github.com/allure-framework/allure2
pytest.main(['-s', '-v', '--capture=sys', '测试用例文件.py','--clean-alluredir', '--alluredir=allure-results'])
os.system(r"allure generate -c -o 测试报告")
```

## [pytest.ini](pytest.ini)
* 改变pytest的默认行为
