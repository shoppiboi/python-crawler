import requests
from bs4 import BeautifulSoup as bs
import time

class Crawler:

    #Issues right now:
        # limiting search to 50-visits-per-domain. Going to change this up a bit soon.

    crawlerDictionary = {}
    totalCrawlers = 0
    limitDictionary = {} # we don't want to flood a site too much, so will keep the limit at 50
    limit = 50 # keep the number of visits to one domain at 50
    domains = [] #keeps track of which domains have been visited

    def __init__(self, name, link, eyedee, depth, limited):

        #passing variables from main.py to class instance
        Crawler.totalCrawlers += 1

        self.name = name
        self.link = link
        self.domain = "/".join(self.link.split("/", 3)[:3]) # stores the domain name of the link assigned

        self.eyedee  = eyedee #eyedee - ID - of the bot in the Dictionary
        self.depth = depth
        self.limited = limited

        #self.variable - initialization
        self.newLinks = []
        self.soup = bs # creates an instance of the BeautifulSoup class
        self.siteContent = ""

        #print(self.name)   - for testing purposes

        #self.methods
        if self.depth >= 1:
            self.checks()
            

    def checks(self): #performs some basic checks

        if self.domain not in Crawler.domains: # adds the domain to the visited-list 
            Crawler.domains.append(self.domain)
            Crawler.limitDictionary[self.domain] = 0

        if self.limited: # if the crawler is in a limited state, will visit each domain only 50 times
            if Crawler.limitDictionary[self.domain] < 50:
                self.run()
            else:
                print(self.domain + " has been visisted " + str(Crawler.limitDictionary[self.domain]) + " times.")
        else:
            self.run()
            
    def run(self):

        #print(self.linkBase)
        if str(self.link).startswith("http") or str(self.link).startswith("https"):
            time.sleep(0.3) # take a breather. We sending a lot of requests to the sites
            
            self.response = requests.get(self.link)
            if self.response.status_code == 200:

                self.soup = bs(self.response.text, 'html.parser') #create response to-be-used in methods

                self.newLinks = self.traverse(self.soup)
                self.p_text = self.sitecontent(self.soup)
                self.newLinks = self.cleanuplinks(self.newLinks)
                
                if self.depth > 0:
                    self.spawncrawler() #spawns new crawlers for each link found on the previous website


            elif self.response.status_code == 404:
                print("Link not found")
                Crawler.totalCrawlers -= 1 # we don't want to include 'failed' crawlers in total count
            elif self.response.status_code == 400:
                print("Bad request")
                Crawler.totalCrawlers -= 1 # --||--
            else:
                print("Blocked or can't access the site. Ignore and move on")
                Crawler.totalCrawlers -= 1 # --||--
        
        else:
            print("Not a valid link")

    def robotsteextee(self): # will be implementing a robots.txt respecting property soon...
        print("robots.txt")

    def traverse(self, soup): # goes through the link provided
        linksFound = [] 

        a_tags = soup.findAll('a')
                
        for x in range(len(a_tags)):
            temp = a_tags[x].get('href')
            
            #print(temp) - for debugging

            if temp is None:
                continue
            else:
            
                try:    
                    if 'https' in temp:
                        if 'google' in temp: #don't include further google links
                            continue
                        elif 'youtube' in temp: #will later add functionality to read subtitles
                            continue
                        elif 'khanacademy' in temp: #will mess with Khan a little later
                            continue
                        else:
                            linksFound.append(temp)
                    elif temp[0] == "/":
                        temp = self.domain + temp
                    else:
                        continue
                except IndexError:
                    continue
            
            
        return linksFound
    

    def cleanuplinks(self, newLinks): # makes the links found more 'clean' and adds them to a new list

        freshList = []

        for x in newLinks:
            if x not in freshList:
                if '/url?q=' in x: #if the link is a normal link
                    x = x.replace('/url?q=', '')
                elif '/imgres?imgurl' in x: #if the link is for an image
                    x = x.replace('/imgres?imgurl=', '')
                x = x.split('&sa')[0]
                freshList.append(x)
        
        return freshList
        #print(newLinks)

    def sitecontent(self, soup):
        p_tags = soup.findAll('p') # find all 'paragraphs'
        return p_tags

    def readcontent(self):
        print("reading content of site")

    # Crawler parameters - name, link, eyedee, depth

    #should clarify:
        #   Child Crawlers are named after their parents.
        #   So if the parent name is Craw 0; then the name of its first child will be "Craw 0-0"...
        #   ... so on and so forth. So a crawler named Craw 5-4-25-6 would be the 7th child of Craw 5-4-25

    def spawncrawler(self): # creates a new crawler for each link found in the previous site
        newDepth = self.depth - 1
        eyedeeBase = str(self.eyedee)
        for x in range(len(self.newLinks)):
            eyedee = eyedeeBase + str(x)
            eyeDeeNo = int(eyedee)
            newName = self.name + "-" + str(x)
            Crawler.crawlerDictionary[eyeDeeNo] = Crawler(newName, self.newLinks[x], eyeDeeNo, newDepth, True)