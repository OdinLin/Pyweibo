Pyweibo
=========

这是我关于新浪微博的python函数

主要是获取新浪微博的一些数据，例如转发数，评论数，微博用户的各种数据，以便以后的数据 挖掘之用，没有用到微博官方的api，因为我觉得官方的api限制太蛋疼，感觉很不爽

文件介绍： 带Util后缀的都是基本功能类，为Pyweibo调用，而用户自己写的函数就直接和Pyweibo这个类交互 就行了

如 weiboUtil.py 是去获取微博数据的基本类，如登录，获取用户数据等 visualizationUtil.py 是数据可视化的类，例如 可以生成可以用可视化软件Gephi打开的dot可是文件 redisUtil.py 和 mongoDBUtil.py 是文档型数据库的功能类，当文件很大或者分析用时 选择调用（不过 很多功能还没实现哦）

还有其他的组件 例如轻量级的mapreduce，这个以后慢慢研究使用

sentimentUtil.py 这个是近期研究的 多微博的情感分析 还没完成哦

使用例子
-

import Pyweibo

pyweibo = Pyweibo.Pyweibo() pyweibo.analyseFollowsFansInfo('1220349643') #分析粉丝和关注者的数据

#####获取单个用户的数据
profile = pyweibo.getPersonalProfile() 
print profile
#####获取用户的微博
pyweibo.getPersonalFeeds(2145291155, './data2') #获取用户的微博
#####产生一个微博的转发路径图（支持多重转发）
pyweibo.generateRepostMap('http://weibo.com/1763362173/zbGgn0e8U', max=10000) 

有些东西还是根据近期阅读的《社交网站的数据挖掘和分析》专门真出来的东西，因为本着的是学习各类知识的 目的来研究编写这些代码的所以在构架上，没有优化处理（高手应该一看就出来了吧）。

所以如果有什么意见高见的 请顺便和我联系 heyflypig@gmail.com 共同学习进步