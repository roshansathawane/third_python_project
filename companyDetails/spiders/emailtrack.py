
import random
import cx_Oracle
import scrapy
import re
from scrapy_selenium import SeleniumRequest # type: ignore
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor # type: ignore

class EmailtrackSpider(scrapy.Spider):
    name = 'emailtrack'
    uniqueemail = set()
    uniquephone = set()

    def __init__(self, *args, **kwargs):
        super(EmailtrackSpider, self).__init__(*args, **kwargs)
        self.token_number = kwargs.get('token_number')
        self.company_urls = eval(kwargs.get('company_urls', '[]'))  
        self.start_urls = self.company_urls

    def start_requests(self):
        for website in self.start_urls:
            yield SeleniumRequest(
                url=website,
                wait_time=3,
                screenshot=True,
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):
        links = LxmlLinkExtractor(allow=()).extract_links(response)
        Finallinks = [str(link.url) for link in links]
        links = [link for link in Finallinks if any(keyword in link.lower() for keyword in ['contact', 'about'])]

        links.append(str(response.url))
        first_link = links.pop(0)

        yield SeleniumRequest(
            url=first_link,
            wait_time=3,
            screenshot=True,
            callback=self.parse_link,
            dont_filter=True,
            meta={'links': links}
        )

    def parse_link(self, response):
        links = response.meta['links']
        html_text = response.text
        email_list = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', html_text)
        
        phone_patterns = [
            r'\b[6-9]\d{9}\b',
            r'\b91[6-9]\d{9}\b',
            r'\b\+91[6-9]\d{9}\b',
            r'\b\d{6}-\d{6}\b',
            r'\+\d{2}-\d{3}-\d{7}\b',
            r'\b\d{3}[\s–-]\d{7}\b',
            r'\b\d{4}[\s–-]\d{7}\b',
            r'\b0\d{3}[\s–-]\d{7}\b',
            r"\b\d{11}\b",
            r'\(\d{3}\) \d{3}-\d{4}',
            r'\d{4}-\d{3}-\d{4}',
            r'\d{2} \d{2}-\d{8}',
            r'\d{2} \d{4}-\d{7}',
            r'\d{2} \d{10}',
            r'\b\d{3}\s\d{4}\s\d{3}\b'
        ]

        phone_list = set()
        for pattern in phone_patterns:
            phone_list.update(re.findall(pattern, html_text))

        self.uniqueemail.update(email_list)
        self.uniquephone.update(phone_list)

        if links:
            next_link = links.pop(0)
            yield SeleniumRequest(
                url=next_link,
                callback=self.parse_link,
                dont_filter=True,
                meta={'links': links}
            )
        else:
            final_emails = list(self.uniqueemail)
            final_phones = list(self.uniquephone)
            result = {
                "emails": final_emails,
                "phones": final_phones
            }
            print('final_emails------------'+str(final_emails))
            print('final_phones------------'+str(final_phones))
           

           