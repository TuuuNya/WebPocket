from lib.pocket import Pocket


class WebPocket(Pocket):
    def run(self):
        self.cmdloop()


if __name__ == '__main__':
    app = WebPocket()
    app.run()
