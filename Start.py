import os
import subprocess
from threading import Thread, active_count
from time import sleep

try:
    from mcrcon import MCRcon
except:
    os.system('pip install mcrcon')
    from mcrcon import MCRcon


def crash():
    returs = []
    with open('logs/latest.log', 'r') as f:
        s = f.read().strip().split('\n')
    s = s[len(s) - 50:len(s)]
    for i in s:
        if 'INFO' in i and 'C2ME' in i:
            pass
        elif 'moved too quickly!' in i or 'the advancement' in i:
            pass
        else:
            returs.append(i)
    return returs


class config:
    def __init__(self):
        self.settings = "java -server -Xmx15G -Xms512M -Xmn256M -rcon.password=H34T69 -XX:+OptimizeFill -jar forge.jar nogui"
        self.file = 'protities.ixt'
        if self.__chek():
            pass
        else:
            print('Файл настроек создан')
            self.__creat()
            exit()

    def open(self):
        with open(self.file, 'r') as f:
            data = f.read()
            return data

    def __creat(self):
        with open(self.file, 'w') as f:
            f.write(self.settings)

    def __chek(self):
        if os.path.exists(self.file):
            return True


class server(config):
    def __init__(self):
        super().__init__()
        self.error = 0
        self.works = False

    def server(self):
        conf = self.open()
        self.works = True
        try:
            self.srv = subprocess.Popen(conf, stdin=subprocess.DEVNULL)
            self.srv.communicate()
        except:
            print(crash())
            self.error += 1
        self.works = False


class control(server):
    def __init__(self) -> None:
        super().__init__()

    def restart(self):
        if self.poll.is_alive():
            self.__stop()
        else:
            pass
        sleep(5)
        self.launch()

    def __stop(self) -> None:
        if self.works or self.poll.is_alive():
            self.srv.kill()

    def launch(self):
        self.poll = Thread(target=self.server, name='MineSRV')
        self.poll.start()

    def it_works(self) -> bool:
        if self.works:
            if self.poll.is_alive():
                return True
        return False

    def progress(self):
        self.launch()
        while self.error < 10:
            count = active_count()
            if count == 2:
                pass
            elif count == 1:
                self.launch()
                self.error += 1
                print(crash())
            elif count >= 6:
                self.__stop()
            sleep(30)


if __name__ == '__main__':
    srv = control()
    srv.progress()
