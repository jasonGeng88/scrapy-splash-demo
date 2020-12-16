

Scrapy + Splash Demo 示例
===========================


本示例基于scrapy和splash技术，实现的爬取去哪儿机票价格最优的一个Demo
verify pr comments

****
###　　　　　　　　　　　　Author:Jason
###　　　　　　　　　 E-mail:372922638@qq.com

===========================

## 技术介绍
* scrapy: 一个基于Python实现的爬虫框架，提供了各种强大的功能，来帮助完成爬虫工作
* splash：提供基于js的页面渲染，帮助完成动态网站的加载

## 运行
### 运行splash

    docker run -p 8050:8050 scrapinghub/splash
### 安转Python依赖包

	pip install -r requirements.txt
	
### 配置MySQL（或修改存储方式）
	
	DB_CONNECT = {
   		'db': 'test',
   		'user': 'root',
   		'passwd': '111111',
   		'host': '127.0.0.1',
   		'charset': 'utf8',
   	 	'use_unicode': True,
	}	
	
### 运行爬虫

	scrapy crawl qunar	

## 参考
[https://doc.scrapy.org/en/1.3/intro/overview.html](https://doc.scrapy.org/en/1.3/intro/overview.html)
[https://github.com/scrapy-plugins/scrapy-splash](https://github.com/scrapy-plugins/scrapy-splash)
