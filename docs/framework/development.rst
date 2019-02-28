====================
模块开发指南
====================


让WebPocket更加好用，需要大家的共同努力。

欢迎大家一起来开发模块，交流安全技术，一起提升安全技能。

我会长期坚持维护该模块库，欢迎大家加入。共勉。

模块基本结构
-------------

基本代码： ::

    import requests
    from lib.BaseExploit import BaseExploit
    from lib.ExploitOption import ExploitOption


    class Exploit(BaseExploit):

        def __init__(self):
            super(Exploit, self).__init__()
            self.update_info(info={
                "name": "模块名称 可用于检索",
                "description": "模块描述 可用于检索",
                "author": ["作者， 可以填写多个"],
                "references": [
                    "参考资料/漏洞来源网址，可填写多个",
                ],
                "disclosure_date": "漏洞发现时间",
                "service_name": "服务名称，如：phpcms、zabbix、php、apache",
                "service_version": "服务版本",
            })

            # 注册模块所需的参数， required为True的模块，默认值请设置为None
            self.register_options([
                ExploitOption(
                    name="host",
                    required=True,
                    description="The target domain",
                    value=None
                ),
                ExploitOption(
                    name="password",
                    required=True,
                    description="webshell password",
                    value=None
                ),
            ])

        # check 方法仅做漏洞检测，不可进行攻击
        # 测试存在漏洞调用 self.results.success方法，传入结果
        # 测试不存在漏洞调用 self.results.failure 传入错误信息
        def check(self):
            webshell = "http://www.hackersb.cn/shell.php"
            if len(webshell):
                self.results.success(
                    message="Target {} has vul".format(self.options.get_option("host"))
                )
            else:
                self.results.failure(error_message="Target {} no vulnerability".format(self.options.get_option("host")))
            return self.results

        # exploit方法为攻击模块 结果同check方法一样处理
        # 注意：不要写可以导致系统崩溃的Exploit方法。
        def exploit(self):
            requests.get(self.options.get_option("host"))
            webshell = "http://www.hackersb.cn/shell.php"
            if len(webshell):
                self.results.success(
                    data={
                        "target": self.options.get_option("host"),
                        "webshell": webshell
                    },
                    message="Webshell: {}".format(webshell)
                )
            else:
                self.results.failure(error_message="No vulnerability")
            return self.results

撰写模块
---------

这里以redis未授权漏洞为例。

首先建立文件： ``/modules/exploits/server/redis_unauthorized.py``

引入 ``BaseExploit`` 类和 ``ExploitOption`` 类，并且写下 ``Exploit`` 类，继承 ``BaseExploit`` 类

所有的模块都必须继承 ``BaseExploit`` 类且类名必须为 ``Exploit`` ， ``ExploitOption`` 用于注册模块参数。

声明Exploit类
--------------

首先撰写类 ::

    from lib.BaseExploit import BaseExploit
    from lib.ExploitOption import ExploitOption


    class Exploit(BaseExploit):
        pass

完成__init__方法
-----------------

然后补全 ``__init__`` 方法： ::

    def __init__(self):
        super(Exploit, self).__init__()
        self.update_info({
            "name": "redis unauthorized",
            "description": "redis unauthorized",
            "author": ["unknown"],
            "references": [
                "https://www.freebuf.com/column/158065.html",
            ],
            "disclosure_date": "2019-02-28",
            "service_name": "redis",
            "service_version": "*",
        })
        self.register_options([
            ExploitOption(
                name="host",
                required=True,
                description="The IP of the machine to be tested",
                value=None
            ),
            ExploitOption(
                name="timeout",
                required=False,
                description="The timeout for connecting to redis",
                value=10,
            ),
            ExploitOption(
                name="port",
                required=False,
                description="redis port",
                value=6379
            )
        ])

这里来解释一下，首先看 ``__init__`` 方法的第一行： ::

    super(Exploit, self).__init__()

这一行是必须的，需要调用父类的 ``__init__`` 方法初始化模块。

随后使用 ``self.update_info`` 方法更新的模块信息： ::

    self.update_info({
        "name": "redis unauthorized",
        "description": "redis unauthorized",
        "author": ["unknown"],
        "references": [
            "https://www.freebuf.com/column/158065.html",
        ],
        "disclosure_date": "2019-02-28",
        "service_name": "redis",
        "service_version": "*",
    })

然后使用 ``self.register_options`` 方法注册三个参数，分别是 ``host``, ``timeout``, ``port``，

 * host 表示需要测试漏洞的主机ip
 * timeout 表示连接redis超时时间
 * port 表示redis端口

代码如下： ::

        self.register_options([
            ExploitOption(
                name="host",
                required=True,
                description="The IP of the machine to be tested",
                value=None
            ),
            ExploitOption(
                name="timeout",
                required=False,
                description="The timeout for connecting to redis",
                value=10,
            ),
            ExploitOption(
                name="port",
                required=False,
                description="redis port",
                value=6379
            )
        ])

完成check方法
--------------

check方法主要写检测漏洞是否存在，不可存在攻击行为。 代码如下： ::

    def check(self):
        host = self.options.get_option("host")
        port = int(self.options.get_option("port"))
        timeout = self.options.get_option("timeout")
        try:
            socket.setdefaulttimeout(timeout)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send(bytes("INFO\r\n", encoding="utf-8"))
            result = s.recv(1024)
            if bytes("redis_version", encoding="utf-8") in result:
                self.results.success(
                    data={
                        "host": host,
                        "port": port,
                    },
                    message="Host {} exists redis unauthorized vulnerability".format(host)
                )
            else:
                self.results.failure(
                    error_message="Host {} does not exists redis unauthorized vulnerability".format(host)
                )
        except Exception as e:
            self.results.failure(error_message=e)
        return self.results

首先前三行使用 ``self.options.get_option()`` 方法获取模块参数。

然后执行了exp过程。

执行成功，发现存在漏洞，调用了 ``self.results.success`` 方法，传入数据和成功信息： ::

    self.results.success(
        data={
            "host": host,
            "port": port,
        },
        message="Host {} exists redis unauthorized vulnerability".format(host)
    )

漏洞不存在则执行了 ``self.results.failure`` 方法，传入失败信息： ::

    self.results.failure(
        error_message="Host {} does not exists redis unauthorized vulnerability".format(host)
    )

check方法最后一行一定要返回 ``self.results`` 出来。 ::

    return self.results


完成exploit方法
----------------

该漏洞比较简单，所以可以不实现exploit方法，可直接return self.check方法。 ::

    def exploit(self):
        return self.check()

exploit方法也一定要返回 ``self.results`` 出来， 因为check方法也是返回 ``self.results`` ，所以这里可以直接调用 ``self.check()`` 。
