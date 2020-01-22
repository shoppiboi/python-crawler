from crawler import Crawler as cr #imports the Crawler class from crawler.py

#to convert to exe - To open the application run this line in cmd: auto-py-to-exe

googleDefault = "http://www.google.com/search?q=" #search link format. Just need to add search parameters
searchLinks = []
Crawlers = {}
crawlerCount = 0

def get_search_link(google, term): # separates and returns search links in correct format

    if ("," in term):
        term = term.replace(",", "")

    if (" " in term):
        term = term.replace(" ", "+", term.count(" "))

    return google + term


def get_input():
    return input("Search terms? (Seperate each term with a comma): ")


def get_depth():
    return input("Depth? ")

    
def main():

    terms = get_input()
    depth = get_depth()
    
    termList = terms.split(", ")

    for y in termList:
        Glink = get_search_link(googleDefault, y)
        searchLinks.append(Glink)
    

    for z in range(len(searchLinks)):
        
        crawlerName = "Craw" + " " + str(z)
        crawlerInst = cr(crawlerName, searchLinks[z], crawlerCount, int(depth), True)
        Crawlers[crawlerCount] = crawlerInst

    #cr.crawlerDictionary = Crawlers  - dictionary of crawlers to be made later

    print("Total number of Crawlers created: " + str(cr.totalCrawlers))


if __name__ == "__main__":
    main()