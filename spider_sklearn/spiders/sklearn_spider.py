import scrapy
import re
from spider_sklearn.mysql_util import MysqlUtil


class SklearnSpider(scrapy.Spider):  # 使用debug文件进行运行，运行参数为：crawl sklearn
    name = "sklearn"
    allowed_domains = ["scikit-learn.org"]  # 域名
    start_urls = [
        "https://scikit-learn.org/stable/modules/classes.html"  # 网页
    ]
    mysql_util = MysqlUtil('10.28.0.196', 'AI_admin', '#O2hs7lSjug5ePEY', 'AI_config')  # 数据库配置
    sklearn_names = ['cluster', 'isotonic', 'calibration', 'cluster.bicluster', 'compose', 'covariance',
                     'cross_decomposition', 'datasets', 'decomposition', 'discriminant_analysis', 'dummy', 'ensemble',
                     'exceptions', 'feature_extraction', 'feature_selection', 'gaussian_process', 'impute',
                     'kernel_approximation', 'kernel_ridge', 'linear_model', 'manifold', 'metrics', 'mixture',
                     'model_selection', 'multiclass', 'multioutput', 'naive_bayes', 'neighbors', 'neural_network',
                     'pipeline', 'preprocessing', 'random_projection', 'semi_supervised', 'svm', 'tree',
                     'utils']  # 需要爬取的算法包名

    def parse(self, response):
        for sklearn_name in self.sklearn_names:
            sklearn = response.xpath('//td/a[@class="reference internal"]')  # 获取sklearn信息载体
            urls = sklearn.xpath('@href').re('^generated/sklearn.' + sklearn_name + '.[A-Z][A-Za-z.]+')  # 获取详情url
            func_names = sklearn.xpath('code/span/text()').re('^' + sklearn_name + '.[A-Z][A-Za-z.]+')  # 获取方法名
            if len(urls) == len(func_names):  # 如果长度相同，表示数据没有混乱
                for i in range(len(func_names)):
                    func_name = re.search(r'[A-Z][A-Za-z.]+$', func_names[i]).group()  # 正则表达式抽取方法名
                    sklearn_func_id = self.mysql_util.insert_func(func_name, sklearn_name)  # 方法名存入数据库，返回当前存入id
                    request = scrapy.Request('https://scikit-learn.org/stable/modules/' + urls[i],
                                             meta={'sklearn_func_id': sklearn_func_id}, callback=self.parse_arg)  # 模拟请求
                    yield request

    def parse_arg(self, response):
        sklearn_func_id = response.meta['sklearn_func_id']  # 获取数据库对应的方法id
        sklearn_arg = response.xpath('//td[@class="field-body"]/dl')[0]  # 获取参数信息载体
        arg_names = sklearn_arg.xpath('dt/strong/text()').extract()  # 获取参数名
        arg_values = sklearn_arg.xpath('dt/span[@class="classifier"]/text()').extract()  # 获取参数详情信息
        arg_docs = sklearn_arg.xpath('dd/p').extract()  # 获取参数介绍
        if len(arg_names) == len(arg_values) & len(arg_docs) == len(arg_values):
            for i in range(len(arg_names)):
                if re.search(r'optional', arg_values[i]):
                    self.mysql_util.insert_arg(arg_names[i], sklearn_func_id, arg_values[i], 1, arg_docs[i])  # 参数存入数据库
                else:
                    self.mysql_util.insert_arg(arg_names[i], sklearn_func_id, arg_values[i], 0, arg_docs[i])  # 参数存入数据库

# if re.search(r'optional', 'float, optional, default: 0.5'):
#     print('yes')
# else:
#     print('no')
