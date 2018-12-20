# spider_sklearn快速开始
### 一.配置：
> 注意：请使用项目自带的虚拟环境

1. 进入spiders文件夹下找到`SklearnSpider`类，所有配置信息如下：
```
name = "sklearn"  # 要执行的spider的名字
allowed_domains = ["scikit-learn.org"]  # 域名
start_urls = [
    "https://scikit-learn.org/stable/modules/classes.html"  # 网页
]
mysql_util = MysqlUtil('localhost', 'root', '1234', 'AI_config')  # 数据库配置
sklearn_names = ['cluster', 'isotonic']  # 需要爬取的算法包名
```
建议修改项：`mysql_util`,`sklearn_names`
2. 运行及debug配置：

配置好了上述环境之后，其实就可以直接在根目录下执行`scrapy crawl <spider名>`(初始为：`scrapy crawl sklearn
`)进行爬取了

如果想要进行debug也可以直接执行`debug.py`文件，传入参数为`crawl <spider名>`(初始为：`scrapy crawl sklearn`)

3. 其他：

所有的数据库操作默认在`mysql_util`中，默认在初始化类`MysqlUtil`时创建数据库连接，所有数据库操作使用同一个连接