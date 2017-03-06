# Scrape-Utils

It provides a utilities to allow scraping

On each request, it changes the User agents and pick a different proxy

Features:

- Random User Agents
- Random Proxy List

---

## Install 

    pip install scrape-utils 
    
    
## Use to request a page

    import scrape_utils 
    from bs4 import BeautifulSoup
    
    url = "http://exmaple.com"
    r = scrape_utils.request(url)
    soup = Beautifulsoup(r.content, "html.parser")
    
    

## Use download images or content

    import scrape_utils 
    
    url = "http://example.com/xysh.png"
    path = scrape_utils.download(url, "/tmp")
    
    
    
    
    