from aylienapiclient import textapi
import threading
import time,sys
import urllib.request
from aylienapiclient.errors import HttpError

#Array of urls
urls = ["https://www.google.com", "https://www.youtube.com", "https://www.facebook.com", "https://www.baidu.com", "https://www.yahoo.com", "https://www.wikipedia.org", "https://www.google.co.in", "https://www.qq.com", "https://www.tmall.com", "https://www.sohu.com", "https://www.google.co.jp"]

class Classify(object):
	def __init__(self):
		#Api key and app id
		self.client = textapi.Client("39d4b4fd","0d7bfc7ae077cd16cbedec8e216994f7")
		# self.client = textapi.Client("3d609645", "58f1c76952ff127eb2d2417484850657")
	
	#function that fetches the categories from the api
	def categorize(self,url,result):
		#If the api cannot fetch categories, mark it uncategorized
		ans = {'url': url , 'categories' : ('Uncategorized','Uncategorized') }
		classifications = self.client.ClassifyByTaxonomy({"url": url, "taxonomy": "iab-qag"})
		ctgs = classifications['categories']
		if ctgs:
			sub = ctgs[0]
			cat = [x for x in ctgs if (x['id'] in sub['id'] and '-' not in x['id'])]
			ans['categories'] = (cat[0]['label'],sub['label'])
		#As it is running on thread append the result in the final array
		result.append(ans)
		per = round(len(result)/len(urls)*100,1)
		#Below code to print progress of the multithread http request
		sys.stdout.write("\rProgress "+str(per)+"%")
		sys.stdout.flush()

	#function where an array can be passed and it returns array of dict containing url and categories 
	def urlarray(self,ar):
		val = []
		print("Started ....")
		#Initiate threads
		threads = [threading.Thread(target=c.categorize, args=(url,val)) for url in urls]
		for thread in threads:
		    thread.start()
		for thread in threads:
		    thread.join()
		print("\nDone ....")
		return val	

#Start the program
c = Classify()
category = c.urlarray(urls)	

#Print top 5 from the array
for i in range(5):
	print ("Url: %s | Category: %s | Subcategory: %s" % (category[i]['url'],category[i]['categories'][0],category[i]['categories'][1]))

