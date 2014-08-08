# coding=utf-8

import os
import logging
import testLogger

class SearchWordFromFiles:
    path = ''   #路径
    word = ''   #要搜索的word关键字
    wlength = 0 #word关键字长度
    start = 0   #当前行开始位置
    lineNum = 0 #当前遍历的行号
    isFileHaveWord = False #文件是否包含关键字
    keyWordNum = 0 #文件包含关键字的数量
    logger = None #日志记录
 
    #查询，路径，字符串
    def search(self, path, word):
        self.keyWordNum=0
        self.path = path
        self.word = word
        self.wlength = len(word)
        self.logger=testLogger.getLoggerOnlyFile(path,'LogAnalysis:'+self.word,'LogAnalysis.log')
        self.getFiles(path)
        self.logger.info('The key word number in all is '+str(self.keyWordNum))
        return self.keyWordNum       
 
    #遍历目录下所有文件
    def getFiles(self, path):
        dirs = os.listdir(path) # 列出该目录下所有文件列表
 
        for d in dirs:
            subpath = os.path.join(path, d) #遍历并判断文件or文件夹
            if os.path.isfile(subpath):
                if 'SingleMonkeyTest' in subpath and 'LogcatOfSingleMonkeyTest' not in subpath:
                    self.readFile(subpath)  #如果为文件直接查询
            else:
                self.getFiles(subpath)  #如果为文件夹遍历继续遍历文件
 
    #查询文件中是否存在字符串
    def readFile(self, fileName):
        self.logger.info('Start reading file:' + fileName)
        f = open(fileName, 'r') #打开文件
        self.lineNum = 1   #记录行数
        self.isFileHaveWord = False
        while True:
            line = f.readline() #读取当前行
            if not line:    #如果读取文件则结束则退出
                break
            self.start = 0
            self.searchFromText(line, self.word)
            self.lineNum = self.lineNum + 1
        f.close()   #关闭文件
        self.logger.info('End reading  file.')
        if not self.isFileHaveWord:
            self.logger.info('The file has no key word:' +self.word+'.')
        self.logger.info('------------------------')
 
    #从text中查找word
    def searchFromText(self, text, word):
        tlength = len(text)
        index = text.find(word)
        if index != -1:
            self.isFileHaveWord=True
            self.keyWordNum=self.keyWordNum+1
            self.logger.info('Line number:'+ str(self.lineNum) +' ,index number' + str(self.start + index) + ' has key word:' +self.word+'.')
            self.start = index + self.wlength
            self.searchFromText(text[self.start:tlength], word)
