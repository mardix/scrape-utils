# Scrape-Utils

It provides a utilities to allow scraping

On each request, it changes the User agents and pick a different proxy

Features:

- Random User Agents
- Random Proxy List
- Extract phone numbers
- Extract emails
- Make url request
- Bloom Filter

---

## Install 

    pip install scrape-utils 
    
    
## Get the page content

    import scrape_utils 
    from bs4 import BeautifulSoup
    
    url = "http://exmaple.com"
    content = scrape_utils.get_url(url)
    soup = Beautifulsoup(r.content, "html.parser")
    
    

## Use download images or content

    import scrape_utils 
    
    url = "http://example.com/xysh.png"
    path = scrape_utils.save_file(url, "/tmp")
    
    
## Extract Phone numbers

You can extract phone numbers. 

    import scrape_utils
    txt = "blah blah (753)746-6382 blah blah"
    list_numbers = scrape_utils.extract_phone_numbers(txt)


## Extract Emails

    import scrape_utils
    txt = "blah blah jake@yahoo.com "
    list_emails = scrape_utils.extract_emails(txt)    

---

## Use BloomFilter
    

    from scrape_utils import BloomFilter
    
    bf = BloomFilter()
    bf.add("hello")
    bf.add("jones")

    if "jones" in bf:
        print("It has it")

    if not bf.contains("bossa"):
        print("Not here")
        
        
To use BF with Redis, add `connection`, the redis connection, `key` the key name
to connect to use Redis instead of memory

---

## Use Spider and Task

`Spider` and `Task` come from the `grab` library

https://github.com/lorien/grab

    from scrape_utils import Spider, Task
    import logging
    
    logging.basicConfig(level=logging.DEBUG)
    
    
    class ExampleSpider(Spider):
        def task_generator(self):
            for lang in 'python', 'ruby', 'perl':
                url = 'https://www.google.com/search?q=%s' % lang
                yield Task('search', url=url, lang=lang)
    
        def task_search(self, grab, task):
            print('%s: %s' % (task.lang, grab.doc('//div[@class="s"]//cite').text()))
    
    
    bot = ExampleSpider(thread_number=2)
    bot.run()



