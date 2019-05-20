====================
模块开发指南
====================


让WebPocket更加好用，需要大家的共同努力。

欢迎大家一起来开发模块，交流安全技术，一起提升安全技能。

我会长期坚持维护该模块库，欢迎大家加入。共勉。

概述
-------------

在 WebPocket 中撰写一个完整的模块，需要符合如下要求：

 * 模块必须为一个 ``class`` 且类名为 ``Exploit``
 * ``Exploit`` 类必须继承自 ``BaseExploit`` （通过 ``from lib.BaseExploit import BaseExploit`` 引入 ）
 * 模块必须包含 ``__init__`` 方法，必须调用父类的 ``__init__`` 方法，（通过 ``super(Exploit, self).__init__()`` 调用）
 * 模块必须填写相关信息，使用 ``self.update_info()`` 方法
 * POC的目标目前主要分为 ``http`` 和 ``tcp`` 类型，使用 ``self.register_tcp_target()`` 注册tcp类型的目标。 使用 ``self.register_http_target()`` 注册http类型的目标。
 * 注册以后的目标可以使用 ``self.options.get_option`` 获取其中的参数。
 * ``check`` 方法用来实现检测漏洞，不可存在攻击行为。
 * ``exploit`` 方法用来实现攻击行为，但也不可进行影响服务器正常运行的操作。
 * 在 ``check`` 和 ``exploit`` 方法中，如果测试成功，调用 ``self.results.success()`` 方法保存结果。失败调用 ``self.results.failure()`` 保存结果。
 * 不管 ``check/exploit`` 成功与否，都要最后返回 ``self.results`` （将来可能会移除该要求,但目前暂时还是需要返回。）。

在写模块的过程中，如果使用 ``pycharm`` 可以跟进上述的方法查看代码，方便大家理解，如有任何疑问或者建议，欢迎联系我。

微信：StrikerSb
邮箱：song@secbox.cn

案例：redis未授权检测模块
----------------------------

基本代码： ::

    # 请求redis需要socket 故引入socket
    import socket
    from lib.BaseExploit import BaseExploit


    class Exploit(BaseExploit):
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
            # 因为redis只需要提供ip和端口，所以这里注册tcp的目标。
            self.register_tcp_target(port_value=6379)

        def check(self):
            # 这三个参数都是self.register_tcp_target方法注册的，这里可以直接调用
            host = self.options.get_option("HOST")
            port = int(self.options.get_option("PORT"))
            timeout = int(self.options.get_option("TIMEOUT"))

            # 执行测试的整个过程最好放进try里面，然后在except里面捕获错误直接调用self.results.failure打印出报错。
            try:
                socket.setdefaulttimeout(timeout)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, port))
                s.send(bytes("INFO\r\n", encoding="utf-8"))
                result = s.recv(1024)
                if bytes("redis_version", encoding="utf-8") in result:
                    # 存在漏洞 调用该方法  data可传入一个字典，目前没有什么用，也可以不传。
                    self.results.success(
                        data={
                            "host": host,
                            "port": port,
                        },
                        # 由于可能会执行多个目标，所以结果里面最好写上目标和端口，方便辨认。
                        message="Host {host}:{port} exists redis unauthorized vulnerability".format(host=host, port=port)
                    )
                else:
                    # 不存在漏洞 调用self.results.failure方法传入错误信息。
                    self.results.failure(
                        error_message="Host {host}:{port} does not exists redis unauthorized vulnerability".format(
                            host=host,
                            port=port
                        )
                    )
            except Exception as e:
                # 执行错误，使用self.results.failure传入错误信息。
                self.results.failure(error_message="Host {host}:{port}: {error}".format(host=host, port=port, error=e))
            return self.results

        def exploit(self):
            return self.check()

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
        self.register_tcp_target(port_value=6379)

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

然后使用 ``self.register_tcp_target`` 方法注册了一个tcp类型的目标，这个方法自动为我们注册了如下参数： ::

    self.register_options([
        ExploitOption(name="HOST", required=True, description="The IP address to be tested"),
        ExploitOption(name="PORT", required=True, description="The port to be tested", value=port_value),
        ExploitOption(name="TIMEOUT", required=True, description="Connection timeout", value=timeout_value),
        ExploitOption(name="THREADS", required=True, description="The number of threads", value=threads_value)
    ])

对于我们redis未授权的漏洞，需要HOST和PORT已经够了，所以不需要再注册多余的参数。

如果需要额外注册参数，可以调用 ``self.register_options`` 方法，传入一个list，list包含 ``ExploitOption`` 对象。

``ExploitOption`` 引入方法：``from lib.ExploitOption import ExploitOption``

完成check方法
--------------

check方法主要写检测漏洞是否存在，不可存在攻击行为。 代码如下： ::

    def check(self):
        host = self.options.get_option("HOST")
        port = int(self.options.get_option("PORT"))
        timeout = int(self.options.get_option("TIMEOUT"))

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
                    message="Host {host}:{port} exists redis unauthorized vulnerability".format(host=host, port=port)
                )
            else:
                self.results.failure(
                    error_message="Host {host}:{port} does not exists redis unauthorized vulnerability".format(
                        host=host,
                        port=port
                    )
                )
        except Exception as e:
            self.results.failure(error_message="Host {host}:{port}: {error}".format(host=host, port=port, error=e))
        return self.results

首先前三行使用 ``self.options.get_option()`` 方法获取模块参数。

然后执行了exp过程。

执行成功，发现存在漏洞，调用了 ``self.results.success`` 方法，传入数据和成功信息： ::

    self.results.success(
        data={
            "host": host,
            "port": port,
        },
        message="Host {host}:{port} exists redis unauthorized vulnerability".format(host=host, port=port)
    )

漏洞不存在则执行了 ``self.results.failure`` 方法，传入失败信息： ::

    self.results.failure(
        error_message="Host {host}:{port} does not exists redis unauthorized vulnerability".format(
            host=host,
            port=port
        )
    )

check方法一定要返回 ``self.results`` 出来。 ::

    return self.results


完成exploit方法
----------------

该漏洞比较简单，所以可以不实现exploit方法，可直接return self.check方法。 ::

    def exploit(self):
        return self.check()

exploit方法也一定要返回 ``self.results`` 出来， 因为check方法也是返回 ``self.results`` ，所以这里可以直接调用 ``self.check()`` 。

更多案例
--------------

现在框架大部分功能已经完成了，我自己会开始写一些模块。

大家可以参考我已经写好的模块，来完成自己的模块。

所有模块都在github仓库中modules目录下。
