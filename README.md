# 《Redis应用实例》随书示例代码



这个代码库展示的是《Redis应用实例》一书的随书示例代码，如果这些代码对你有帮助的话，欢迎通过购买图书来支持我的工作，谢谢！

关于《Redis应用实例》的更多信息请参考该书主页：[huangz.works/rediscookbook/](https://huangz.works/rediscookbook/)

软件需求：Python 3.12+，Redis 7.4+，redis-py 5.1.0b7+

| 章号 | 标题               | 代码及其描述                                                 |
| ---- | ------------------ | ------------------------------------------------------------ |
| 1    | 缓存文本数据       | ``Cache``——使用字符串实现的文本缓存程序<br />``JsonCache``——使用字符串和JSON实现的多项数据缓存程序<br />``HashCache``——使用哈希实现的多项数据缓存程序 |
| 2    | 缓存二进制数据     | ``BinaryCache``——使用字符串实现的二进制文件缓存程序          |
| 3    | 锁                 | ``Lock``——基本的锁（使用字符串实现）<br />``AutoReleaseLock``——带自动释放功能的锁（使用字符串实现） |
| 4    | 带密码保护的锁     | ``IdentityLock``——带密码保护功能的锁（使用字符串实现）       |
| 5    | 自增数字ID         | ``IdGenerator``——使用字符串实现的ID生成器<br />``HashIdGenerator``——使用哈希实现的ID生成器 |
| 6    | 计数器             | ``Counter``——使用字符串实现的计数器<br />``HashCounter``——使用哈希实现的计数器 |
| 7    | 唯一计数器         | ``UniqueCounter``——使用集合实现的唯一计数器<br />``HllUniqueCounter``——使用HyperLogLog实现的唯一计数器 |
| 8    | 速率限制器         | ``RateLimiter``——速率限制器（使用字符串实现）                |
| 9    | 二元操作记录器     | ``BinaryRecorder``——二元操作记录器（使用位图实现）           |
| 10   | 资源池             | ``ResourcePool``——资源池程序（使用集合实现）                 |
| 11   | 紧凑字符串         | ``CompactString``——紧凑字符串程序（使用字符串实现）          |
| 12   | 数据库迭代器       | ``DbIterator``——数据库迭代器程序（使用``SCAN``实现）<br />``DbSampler``——迭代式数据库取样程序（使用``SCAN``和``TYPE``实现）<br />``random_key_generator()``——随机类型键生成器 |
| 13   | 流迭代器           | ``StreamIterator``——使用``XRANGE``命令实现的流迭代器<br />``StreamIterator``——使用``XREAD``命令实现的流迭代器 |
| 14   | 消息队列           | ``MessageQueue``——消息队列程序（使用流实现）<br />``Chat``——直播弹幕程序（使用流实现） |
| 15   | 标签系统           | ``Tag``——标签系统程序（使用集合实现）                        |
| 16   | 自动补全           | ``AutoComplete``——自动补全程序（使用有序集合实现）           |
| 17   | 抽奖               | ``Lottery``——抽奖程序（使用集合实现）                        |
| 18   | 社交关系           | ``Relation``——社交关系程序（使用有序集合实现）               |
| 19   | 登录会话           | ``Session``——会话程序（使用字符串实现）                      |
| 20   | 短网址生成器       | ``UrlShorty``——短网址生成器（使用字符串和哈希实现）<br />``base62()``——将数字从10进制转换为62进制的函数 |
| 21   | 投票               | ``Vote``——投票程序（使用集合实现）                           |
| 22   | 排行榜             | ``Ranking``——排行榜程序（使用有序集合实现）                  |
| 23   | 分页               | ``Pagging``——分页程序（使用列表实现）                        |
| 24   | 时间线             | ``Timeline``——时间线程序（使用有序集合实现）                 |
| 25   | 地理位置           | ``Location``——地理位置程序（使用地理位置索引实现）           |
| 26   | 先进先出队列       | ``FifoQueue``、``FifoQueueR``——先进先出队列（使用列表实现）  |
| 27   | 定长队列和淘汰队列 | ``FixedLengthQueue``——定长队列（使用列表实现）<br />``FadedQueue``——淘汰队列（使用列表实现） |
| 28   | 栈/后进先出队列    | ``Stack``——栈（使用列表实现）                                |
| 29   | 优先队列           | ``PriorityQueue``——优先队列（使用有序集合实现）              |
| 30   | 循环队列           | ``CircularQueue``——循环队列（使用列表实现）<br />``UniqueCircularQueue``——无重复元素的循环队列（使用列表实现） |
| 31   | 矩阵               | ``ListMatrix``——使用列表实现的矩阵程序<br />``BitmapMatrix``——使用位图实现的矩阵程序 |
| 32   | 逻辑矩阵           | ``LogicalMatrix``——逻辑矩阵程序（使用位图实现）<br />``CompactLogicalMatrix``——紧凑逻辑矩阵程序（使用位图实现） |



## 版权声明

版权所有©2024，黄健宏。

本项目中的代码受到版权和著作权保护，请勿在未授权的情况下在商业场景中使用本项目。

Copyright©2024, the code in this project is protected by copyright and authorship, please do not use this project in commercial scenarios without authorization.