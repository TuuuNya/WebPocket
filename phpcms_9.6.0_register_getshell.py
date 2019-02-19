from demo.BaseExploit import BaseExploit


class Exploit(BaseExploit):

    def __init__(self):
        super(Exploit, self).__init__()
        self.update_info(info={
            "name": "phpcms 9.6.0 register getshell",
            "description": "phpcms 9.6.0 register page getshell",
            "author": ["unknown"],
            "references": [
                "https://www.hackersb.cn/hacker/219.html",
            ],
            "disclosure_date": "2017-04-14",
            "service_name": "phpcms",
            "service_version": "9.6.0",
        })

    def check(self):
        pass

    def exploit(self):
        exploit_options = self.get_options()
        pass


if __name__ == '__main__':
    exp = Exploit()
    exp.exploit()
