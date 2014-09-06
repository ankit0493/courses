import subprocess, sys

# gets the first link on any webpage
def get_next_target(page):
    copy = page
    repl = ['= ', ' =', ' = ']
    for i in range(0, len(repl)):
        copy = copy.replace(repl[i], "=")

    first_link_start = copy.find("<a")
	   
    if (first_link_start == -1):
        return None
    else:
        first_url_start = copy.find("href=", first_link_start) + len("href=") + 1

        if (copy[copy.find("href=", first_link_start) + len("href=")] == '"'):
            url = copy[first_url_start:copy.find('"', first_url_start)]
        else:
            url = copy[first_url_start:copy.find("'", first_url_start)]

        first_url_end = page.find(url) + len(url) + 1
        return url, first_url_end

# prints out all of the links on a webpage
def get_all_links(page):
    links = []
    while (get_next_target(page) != None):
        url, marker = get_next_target(page)
        links.append(url)
        page = page[marker:]
    return links

# joins two lists, ignoring shared items
def union(a, b):
    [a.append(x) for x in b if x not in a]

def get_page(url):
    try:
        return subprocess.check_output(['curl', '-s', url])
    except subprocess.CalledProcessError as failure:
        sys.exit('\n\033[91mfatal: %s\n\033[0m' % failure)
    
# crawls the web for all links reachable by a seed page
def crawl_web(seed):
    to_crawl = [seed]
    crawled = []
    while to_crawl:
        page = to_crawl.pop()
        if page not in crawled:
            union(to_crawl, get_all_links(get_page(page)))
            crawled.append(page)
    return crawled
  
try:
    start_url = sys.argv[1]
except IndexError:
    sys.exit('\n\033[91mfatal: no seed url given\n\033[0m')

all_links = crawl_web(start_url)
print all_links