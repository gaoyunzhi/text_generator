# -*- coding: UTF-8 -*-
import random
import subprocess
import sys, tty, termios, os

class TextGenerator:
    EMOTIONS = ["", "", "", "", ":)", ":)", "^_^", "~", "~~"]
    DECAY = 0.7
    para_1 = ["你好，欢迎加入读书分享！",
        "你好，欢迎加入读书分享小组！", 
        "你好，欢迎加入我们读书分享！" , 
        "你好，欢迎加入我们读书分享小组！"]

    para_3 = ["我们的Facebook群组在 https://www.facebook.com/groups/reading.sharing/ 欢迎加入我们的讨论。",
        "我们在微信上也有一个读书小组，有兴趣的朋友欢迎联系我的微信fenxiangdushu。",
        ""]

    qq_para_1 = ["不好意思打搅啦！", "不好意思打搅一下~"]
    TAGS = ["读书会", "读书群", "微信读书群", "读书小组", "读书分享", "读书微信群", "微信群"]

    def getText(self, key):
        if self.facebookMode:
            text = self.getFacebookText(key)
        else:
            text = self.getQQText(key)
        self.writeToClipboard(text)    
        return text

    def getQQText(self, key):
        return self.getQQPara1() + \
            "我们在微信上也有一个读书小组，有兴趣的朋友欢迎联系我的微信fenxiangdushu。" + \
            self.getEOL() + self.getPara2() + "欢迎多多交流，分享笔记~" + \
            self.getEOL() + self.getTags()

    def getFacebookText(self, key):
        return self.getPara1() + self.getPara2() + self.getEOL() + \
            self.getPara3(key) + self.getPara4() + self.getEOL() + self.getPara5()
          
    def getPara1(self):
        if not self.intro:
            return "你好！" + self.getEOL() 
        return  random.choice(self.para_1) + self.getEOL() 

    def getQQPara1(self):
        if self.single:
            return "你好，" + random.choice(self.qq_para_1) 
        return "大家好，" + random.choice(self.qq_para_1) 

    def writeToClipboard(self, output):
        process = subprocess.Popen(
            'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        process.communicate(output)

    def getPara2(self):
        book_path = os.path.join(os.path.dirname(__file__), 'books.txt')
        book_file = open(book_path).readlines()
        book_list = []
        param = 1
        for book_name in book_file:
            if random.random() < param:
                book_list.append(book_name.strip())
                param = param * self.DECAY
            if len(book_list) > 5:
                break
        random.shuffle(book_list)
        return "读书分享草创于四年前，致力于分享有深度的好书。我们近期读过的书有" + \
            "，".join(book_list[:5]) + "。"

    def getPara3(self, key):
        if key == "w":
            return self.para_3[1]
        if key == "z":
            return self.para_3[0] + self.getEOL() + self.para_3[1]
        return self.para_3[0]

    def getPara4(self):
        if self.end:
            return "最近读了什么书呀？欢迎加我为Facebook好友，多多交流，分享笔记~"
        return "最近读了什么书呀？欢迎多多交流，分享笔记~"

    def getPara5(self):
        if not self.enableVerification:
            return ""
        return random.choice([
            "请问可以分享一下您的书单吗？作为进群的验证。给您带来不便，还请谅解~",
            "请问可以分享一下您的书单吗？作为进群的验证。带来不便请谅解~"
        ]) + self.getEOL() 

    def getTags(self):
        if not self.tags:
            return ""
        random.shuffle(self.TAGS)
        return "tags: " + ", ".join(self.TAGS[:5])    

    def getEOL(self):
        return random.choice(self.EMOTIONS) + "\n\n" 

    def getch(self):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def flipIntro(self):
        self.intro = not self.intro

    def flipEnd(self):
        self.end = not self.end

    def flipMode(self):
        self.facebookMode = not self.facebookMode # douban and qq mode

    def flipSingle(self):
        self.single = not self.single

    def flipVerification(self):
        self.enableVerification = not self.enableVerification

    def flipTags(self):
        self.tags = not self.tags    

    def __init__(self):
        self.intro = True
        self.end = True
        self.facebookMode = True
        self.single = False
        self.enableVerification = False
        self.tags = False

    def run(self):
        print self.getText("")
        while True:
            key = self.getch()
            if key == "c":
                return
            if key == "i":
                self.flipIntro()
            if key == "e":
                self.flipEnd()
            if key == "f":
                self.flipMode()
            if key == "s":
                self.flipSingle()
            if key == "v":
                self.flipVerification()
            if key == "t":
                self.flipTags()
            print self.getText(key)

TextGenerator().run()




