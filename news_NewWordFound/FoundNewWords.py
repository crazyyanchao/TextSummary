# 基于切分的新词发现是对	新词发现的信息熵方法的改进，降低计算量
import pymongo # PyMongo是MongoDB的Python接口开发包。

db = pymongo.MongoClient().baike.items
def texts():
    for a in db.find(no_cursor_timeout=True).limit(1000000):
        yield a['content']

from collections import defaultdict
from itertools import tee
from tqdm import tqdm
import re
'''Tqdm 是一个快速，可扩展的Python进度条，可以在 Python 长循环中添加一个进度提示信息，用户只需要封装任意的迭代器 tqdm(iterator)。'''

class Find_Words:
    def __init__(self, min_count=10, min_proba=1):
        self.min_count = min_count
        self.min_proba = min_proba
        self.chars, self.pairs = defaultdict(int), defaultdict(int)
        self.total = 0.
    def text_filter(self, texts):
        for a in tqdm(texts):
            for t in re.split(u'[^\u4e00-\u9fa50-9a-zA-Z]+', a):
                if t:
                    yield t
    def count(self, texts):
        for text in self.text_filter(texts):
            self.chars[text[0]] += 1
            for i in range(len(text)-1):
                self.chars[text[i+1]] += 1
                self.pairs[text[i:i+2]] += 1
                self.total += 1
        self.chars = {i:j for i,j in self.chars.iteritems() if j >= self.min_count}
        self.pairs = {i:j for i,j in self.pairs.iteritems() if j >= self.min_count}
        self.strong_segments = {i: self.total*j/(self.chars[i[0]]*self.chars[i[1]]) for i,j in self.pairs.iteritems()}
        self.strong_segments = {i:j for i,j in self.strong_segments.iteritems() if j >= self.min_proba}
    def find_words(self, texts):
        self.words = defaultdict(int)
        self.total_words = 0.
        for text in self.text_filter(texts):
            s = text[0]
            for i in range(len(text)-1):
                if text[i:i+2] in self.strong_segments:
                    s += text[i+1]
                else:
                    self.words[s] += 1
                    self.total_words += 1
                    s = text[i+1]
        self.words = {i:j for i,j in self.words.iteritems() if j >= self.min_count}

fw = Find_Words(16, 1)
fw.count(texts())
fw.find_words(texts())

import pandas as pd
words = pd.Series(fw.words).sort_values(ascending=False)