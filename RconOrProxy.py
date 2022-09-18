import os
from threading import Thread
from time import sleep

try:
    import paho.mqtt.client as mqtt
except:
    os.system('pip install paho.mqtt')
    import paho.mqtt.client as mqtt
try:
    from mcrcon import MCRcon
except:
    os.system('pip install mcrcon')
    from mcrcon import MCRcon


class rcon:
    def __init__(self,ip='127.0.0.1', passwd='B1SArs56AFDb'):
        self.ip = ip
        self.passwd = passwd
        self.connected = False
        self.connect()

    def __connect(self) -> bool:
        try:
            print(f"[Поток Rcon][{self.ip}] Попытка запуска")
            self.rcon = MCRcon(self.ip, self.passwd)
            self.rcon.connect()
            print(f"[Поток Rcon][{self.ip}] Соединение установлено")
            return True
        except Exception as e:
            print(f"[Поток Rcon][{self.ip}] Ошибка запуска: \n{e}")
            return False

    def filter(self,command) -> str:
        if self.connected:
            a = '#help - подсказки\n#stop - выключение сервера\n#reconnect - переподключение без перезапуска приложения\n#save - сохранить мир\n/комманда_для_майна'

            if command[0:1] == '#':
                command= command[1:] #Команды для локалки:
                if command == 're' or command == 'reconnect':self.__connect()
                if 'exit' in command: exit()
                if 'stop' in command or 'restart' in command: #
                    self.send_command('/save-all')
                    self.send_command('/say ПЕРЕЗАПУСК СЕРВЕРА !!!')
                    sleep(10)
                    self.send_command('/stop')
                if 'save' in command: self.send_command('/save-all')
                if 'white' in command:
                    self.send_command(f'/whitelist add {command[6:]}')
            elif command[0:1] == '/': #Команды для сервера:
                return self.send_command(command)
        else:
            self.connect()

    def send_command(self,command) -> str:
        try:
            return self.rcon.command(f'{command}')
        except Exception as e:
            self.connected = False
            print(e)

    def connect(self) -> bool:
        self.connected = self.__connect()
        while self.connected == False:
            sleep(2)
            self.connected = self.__connect()
        return True

class proxy:
    pass
class tg(rcon):
    def __init__(self):
        super().__init__()
        admin = [515944547,931210130]
        import telebot
        from telebot import types  # для указание типов
        bot = telebot.TeleBot('5672650027:AAG6b2Jjj3H8rcbkWItowwF-0FTf7XGF2yk')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("/reconnect")
        btn2 = types.KeyboardButton("/help")
        btn3 = types.KeyboardButton("/statys")
        markup.add(btn1, btn2, btn3)

        def max_length(message:str,user_id):
            if len(message) > 4096:
                for x in range(0, len(message), 4096):
                    bot.send_message(user_id, '{}'.format(message[x:x + 4096]), reply_markup=markup)
                    print(x)
            else:
                bot.send_message(user_id, '{}'.format(message),reply_markup=markup)

        @bot.message_handler(content_types=['text'])
        def get_text_messages(message):
            if message.from_user.id in admin:
                text = message.text
                if '#' in text:
                    text = text.replace("#","/")
                    text = self.send_command(text)
                    print(len(text))
                    #text=self.__send_command(f'{text}')
                    max_length(text,message.from_user.id)
                    #bot.send_message(message.from_user.id,'ghsd\n fae')
                elif '/re' in text or '/reconnect' in text:
                    if self.connect():
                        bot.send_message(message.from_user.id,'Переподключение прошло успешно',reply_markup=markup)
                elif '/help' in text:
                    bot.send_message(message.chat.id,"Забыл каманды?\n"
                                                     "# команда майна\n")
                elif '/statys' in text:
                    text = self.send_command('/list')
                    max_length(text,message.from_user.id)
            #bot.send_message(message.from_user.id, 'Переподключение прошло успешно')

        def chtime():
            while True:
                self.connect()
                text = self.send_command('/list')
                for piple in admin:
                    max_length(text,piple)
                sleep(3600)

        Thread(target=chtime, name='informator').start()
        bot.polling(none_stop=True, interval=2)




class discod:
    pass


if __name__ == '__main__':
    pass
    #Telegram = tg()
    #Rcon = rcon()
    #Rcon.filter('#white Igor2026')

