import requests
from bs4 import BeautifulSoup
import threading

class Tokenize:
    tokenized_array = []
    def __init__(self, keyword):
        self.keyword = keyword

    def tokenize(self):
        tokenized_array = self.keyword.split(' ')
        for word in tokenized_array:
            if (len(word)>=3):
                self.tokenized_array.append(word)
        if (len(self.tokenized_array)<3):
            return self.tokenized_array
        else:
            return []

class Scrapper:
    priority_jobs = []
    jobs = []
    keyword = ''
    urls = ['https://gjirafa.com/Top/Pune?&q=', 'https://jobs.telegrafi.com/?q=','https://kosovajob.com/?q=','https://punaime.org/?s=','https://ofertapune.net/?s=' ]
    classes = ['resultsAll', 'col-sm-12', 'containerLeftJobLists', 'owl-carousel', 'col-md-9']

    def __init__(self, keyword):
        self.keyword = keyword.lower()
        tokenize = Tokenize(keyword)
        self.tokenizedKeyword = tokenize.tokenize()
        self.tokenizedKeyword.insert(0,self.keyword)
        self.startThreading()
        self.outputData()


    def getData(self, url, index):

        for keyword in self.tokenizedKeyword:
            html = requests.get(url+keyword).text
            soup = BeautifulSoup(html, 'html.parser')
            for data in soup.find_all('div', class_=self.classes[index]):
                for a in data.find_all('a'):
                    if ('lokacioni' not in a.get('href')): #per disa faqe
                        if ('http' in a.get('href')):
                            job = a.get('href')
                            # title = a.text
                            if ((job not in self.jobs) and (job not in self.priority_jobs)):
                                if keyword == self.tokenizedKeyword[0]:
                                    self.priority_jobs.append(job)
                                else:
                                    self.jobs.append(job)

    def startThreading(self):
        print ("Duke kerkuar...")
        threads = []
        for i in range(5):
            t = threading.Thread(target=self.getData, args=(self.urls[i], i))
            t.daemon = True
            threads.append(t)
        for i in range(5):
            threads[i].start()
        for i in range(5):
            threads[i].join()

    def outputData(self):
        file = open('Jobs.txt', 'w',  encoding='utf8')
        file.close()
        print (self.priority_jobs)
        print (self.jobs)
        jobs = self.priority_jobs + self.jobs
        print (jobs)
        for job in jobs:
            file = open('Jobs.txt', 'a')
            file.write(job + '\n')
            file.close()
        print ('Output file u krijua me sukses!')
