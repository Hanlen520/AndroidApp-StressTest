# coding=utf-8

import os
import logging
import testLogger

class SearchWordFromFiles:
    path = ''   #·��
    word = ''   #Ҫ������word�ؼ���
    wlength = 0 #word�ؼ��ֳ���
    start = 0   #��ǰ�п�ʼλ��
    lineNum = 0 #��ǰ�������к�
    isFileHaveWord = False #�ļ��Ƿ�����ؼ���
    keyWordNum = 0 #�ļ������ؼ��ֵ�����
    logger = None #��־��¼
 
    #��ѯ��·�����ַ���
    def search(self, path, word):
        self.keyWordNum=0
        self.path = path
        self.word = word
        self.wlength = len(word)
        self.logger=testLogger.getLoggerOnlyFile(path,'LogAnalysis:'+self.word,'LogAnalysis.log')
        self.getFiles(path)
        self.logger.info('The key word number in all is '+str(self.keyWordNum))
        return self.keyWordNum       
 
    #����Ŀ¼�������ļ�
    def getFiles(self, path):
        dirs = os.listdir(path) # �г���Ŀ¼�������ļ��б�
 
        for d in dirs:
            subpath = os.path.join(path, d) #�������ж��ļ�or�ļ���
            if os.path.isfile(subpath):
                if 'SingleMonkeyTest' in subpath and 'LogcatOfSingleMonkeyTest' not in subpath:
                    self.readFile(subpath)  #���Ϊ�ļ�ֱ�Ӳ�ѯ
            else:
                self.getFiles(subpath)  #���Ϊ�ļ��б������������ļ�
 
    #��ѯ�ļ����Ƿ�����ַ���
    def readFile(self, fileName):
        self.logger.info('Start reading file:' + fileName)
        f = open(fileName, 'r') #���ļ�
        self.lineNum = 1   #��¼����
        self.isFileHaveWord = False
        while True:
            line = f.readline() #��ȡ��ǰ��
            if not line:    #�����ȡ�ļ���������˳�
                break
            self.start = 0
            self.searchFromText(line, self.word)
            self.lineNum = self.lineNum + 1
        f.close()   #�ر��ļ�
        self.logger.info('End reading  file.')
        if not self.isFileHaveWord:
            self.logger.info('The file has no key word:' +self.word+'.')
        self.logger.info('------------------------')
 
    #��text�в���word
    def searchFromText(self, text, word):
        tlength = len(text)
        index = text.find(word)
        if index != -1:
            self.isFileHaveWord=True
            self.keyWordNum=self.keyWordNum+1
            self.logger.info('Line number:'+ str(self.lineNum) +' ,index number' + str(self.start + index) + ' has key word:' +self.word+'.')
            self.start = index + self.wlength
            self.searchFromText(text[self.start:tlength], word)
