import requests
import bs4
import os
import re
from bs4 import BeautifulSoup
import time
import urllib3
import sys
import enchant

# set the recursion limit for the breadth first search to run
sys.setrecursionlimit(1500)

# politeness policy implementation for waiting for 1 second before querying again
politeness = 1

# maximum number of urls to crawl
max_url = 1000

# keep a seen list to chek the count of links
seen = []

# keeps track of the list of websites
frontier = []

# visited links are recorded here
depthDict = {}

# counter to store the depth of traversal
depth = 1

# counter to store all the HTML files in a folder
counter = 1

# counter to store all the HTML files in a folder
counter_new = 1

# keywords to keep track of
keywords = []

# create a dictionary using enchant to check the words that are found from the tokenization of the URL are actual
# english words
dictionary = enchant.Dict()

# List to store the links from the 1000 link files, will contain 3000 links
new_list = []

# List to remove duplicates from the links in the new_list,
# checker_list does not have duplicates
checker_list = []

# List to write to take the first 1000 links from the sorted new_list
final_list = []

# List to use to write to the file with the final crawled links
new_final_list = []


# method to use web crawler to find the links in a web page
def web_crawler(url):

    global politeness
    global keywords
    global depth

    # Implementing the politeness policy
    time.sleep(politeness)

    # code checking comment
    #print("*************** "+url+" ************** is getting crawled")


    # request to the page if the page doesn't return then break
    page = requests.get(url)
    if page.status_code != 200:
        return

    # create a soup object using BeautifulSoup
    soup = BeautifulSoup(page.content, 'html.parser')

    # call to the function to save the raw HTML
    write_html_to_file(soup)

    # filter the soup to remove unnecessary content
    soup = filtersoup(soup)

    # check the url(href) from soup in all levels of the bfs tree, if found, break
    for keys in depthDict.keys():
        if url in depthDict[keys]:
            depth = keys
            break

    # comment to check code
    # print("this is the depth:   " + str(depth))

    # increment the depth by 1
    depth = depth + 1

    # Check if the depth is less than 7
    if depth <= 6:
        # for every link from the soup save the href part in url
        for link in soup.find_all('a', href=True):
            url = str(link['href'])
            # filter the links to remove links with #, Main_Page, and other filters
            if "#" not in url and "Main_Page" not in url and ".jpg" not in url and "disambiguation" not in url \
                    and filter_colons(url) and filter_links(url):
                # filter the frontier
                filter_frontier_for_links()
                # filter the frontier to match the keywords
                if filter_frontier(url, link):
                    # check the presence of the link in frontier
                    if "https://en.wikipedia.org/" + url not in frontier:
                        # testing comment
                        print("**************" + url)

                        # append the link to the frontier
                        frontier.append("https://en.wikipedia.org/"+url)

                        # if a link is found that is new add it at that depth
                        if depth not in depthDict.keys():
                            depthDict[depth] = []
                        depthDict[depth].append("https://en.wikipedia.org/"+url)




def write_html_to_file(soup):

    global counter_new

    # writing to file all the HTML content of the soup
    if counter_new <= max_url:
        file = open('/Users/mihirg/PycharmProjects/assignment1/FocusedCrawler/{}.txt'.format(counter_new), 'w')
        file.write(soup.prettify())
        counter_new += 1


# Check if the word is present in the dictionary
# the dictionary is obtained using pyEnchant
def check_word_existence(word):
    boolean_cond = False
    if word != "" and len(word) != 0:
        if dictionary.check(word):
            boolean_cond = True
    return boolean_cond


def breadthfirstsearch(seed):

    # Check if the length of the seen list becomes more than the max url then stop
    if len(seen) > max_url:
        return

    # append the current seed to the seen list
    seen.append(seed)

    # crawl the web for the seed that is passed first
    web_crawler(seed)

    # make the first element of the frontier list to be equal to new seed
    new_seed = frontier[0]

    # remove the new seed element from the frontier
    frontier.remove(new_seed)

    # call bfs on the new seed from frontier
    breadthfirstsearch(new_seed)


# method to filter the soup
def filtersoup(soup):

    # remove all the table tag elements
    for item in soup.findAll('table'):
        item.extract()
    # remove all the divs with class "thumbcaption"
    for thumb in soup.findAll("div", {"class": "thumbcaption"}):
        thumb.extract()
    return soup


# method to filter all the links
def filter_links(link):

    # testing comment
    # print(link)

    # create a regular expression to match relevant links
    pattern = re.compile('^/wiki/(.)*')
    matcher = pattern.match(link)

    if matcher:
        return True
    else:
        return False

# remove the links with a colon because they are administrative links
def filter_colons(link):
    # print(link)
    pattern = re.compile('^/wiki/(.)*:(.)*')
    matcher = pattern.match(link)
    # Reverse the matcher output to match the links that are relevant
    if matcher:
        return False
    else:
        return True


# filter the frontier to remove the links that are images, non textual media...
def filter_frontier_for_links():
    global frontier

    for link in frontier:
        if ".png" in link:
            frontier.remove(link)
        elif ".ogg" in link:
            frontier.remove(link)
        elif ".jpg" in link:
            frontier.remove(link)
        elif ".JPG" in link:
            frontier.remove(link)
        elif ".gif" in link:
            frontier.remove(link)
        elif ".svg" in link:
            frontier.remove(link)
        elif "Main_Page" in link:
            frontier.remove(link)

    return frontier


# method to write all the crawled links less than 1000 in a file with their depth
def writeToFile():

    # testing comment
    # for x in seen:
    #     file.write(x+"\n")

    global counter

    file2 = open('/Users/mihirg/PycharmProjects/assignment1/FocusedCrawler/focusedcrawlerlinksnew.txt', 'w')
    for x in depthDict.keys():
        for link in depthDict[x]:
            if counter <= max_url:
                file2.write(str(x) + " " + link + "\n")
                counter += 1


def final_write():
    global new_list
    global checker_list
    global final_list
    global new_final_list

    # Open the three files that we want to merge from their respective folders
    file1 = open('/Users/mihirg/PycharmProjects/assignment1/FocusedCrawler/focusedcrawlerlinksnew.txt')

    # read the lines from the three files and store the lines in the separate variables
    lines = file1.readlines()

    # Using regular expressions to filter the links in the files
    regex = re.compile('[1](.)*')
    regex2 = re.compile('[2](.)*')
    regex3 = re.compile('[3](.)*')
    regex4 = re.compile('[4](.)*')
    regex5 = re.compile('[5](.)*')
    regex6 = re.compile('[6](.)*')

    # using the regular expressions to filter the links in the file and add them to the list in order of the depth
    for line in lines:
        if regex.match(line):
            new_list.append(line)

    for line in lines:
        if regex2.match(line):
            new_list.append(line)

    for line in lines:
        if regex3.match(line):
            new_list.append(line)

    for line in lines:
        if regex4.match(line):
            new_list.append(line)

    for line in lines:
        if regex5.match(line):
            new_list.append(line)

    for line in lines:
        if regex6.match(line):
            new_list.append(line)

    # Loop through the new_list and store the links that are not duplicates
    for x in new_list:
        if x not in checker_list:
            checker_list.append(x)

    # Update the new_list with the duplicates removed
    new_list = checker_list

    # copy the first 1000 links from the sorted new_list to final_list
    final_list = new_list[:1000]

    # loop through the final list and copy those links that do not have different depths but same urls
    for x in final_list:
        if x[2:] not in new_final_list:
            new_final_list.append(x)

    # write to the file
    file = open('/Users/mihirg/PycharmProjects/assignment1/FocusedCrawler/finallist.txt', 'w')
    for x in new_final_list:
        file.write(x)


# method to match the keywords to the required links
def filter_frontier(link, url):
    global keywords
    # split the link to create tokens, convert tokens to lowercase, convert keywords to lower case and compare
    # if the tokens match then return the link without the underscores and the special charactes
    # tokens are created using regular expressions split
    # we can also use nltk -  word_tokenize for the generation of tokens but eventual checking has to be performed on
    # an english dictionary like opne provided by pyEnchant
    keyword = re.split("[\W_]", link)
    # print('filter_frontier keywords are--------------')
    # print(keyword)
    for x in keywords:
        for y in keyword:
                if x.lower() == y.lower() or x.lower() in url.text:
                        return link


# method to perform breadth first crawling of the seed given in the question
def task3():

    seed = "https://en.wikipedia.org/wiki/Carbon_footprint"

    depthDict[1] = [seed]

    global keywords

    # keywords takes the keywords entered by the user
    keywords = input("Enter the keywords that you want to search for and separate them by a comma(,)").split(",")

    breadthfirstsearch(seed)

    writeToFile()

    final_write()


# Declaring the main function in Python
def main():
    task3()
    # testing comment
    # breadthfirstsearch("https://en.wikipedia.org/wiki/Time_zone")

    # breadthfirstsearch("https://en.wikipedia.org/wiki/Electric_car")

    # breadthfirstsearch("https://en.wikipedia.org/wiki/Carbon_footprint")


# Checking if the program is being run by itself or imported from another module
if __name__ == '__main__':
    # print ('This program is being run by itself');
    main()
else:
    print('the program is imported from another module')
