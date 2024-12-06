import scrapy
import csv
from datetime import datetime
import scrapy
import csv
import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quotes_data = []  # Variable to store scraped data

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            text = quote.css('.text::text').get()
            author = quote.css('.author::text').get()
            tags = quote.css('.tags .tag::text').getall()

            # Save each quote as a dictionary in the list
            self.quotes_data.append({
                'text': text,
                'author': author,
                'tags': tags,
            })

        # Debug: Print to ensure data is captured
        self.log(f"Captured quotes: {self.quotes_data}")

    def closed(self, reason):
        # This method is called after the spider finishes
        # Use this to save data to a file manually if needed
        with open('quotes_data.json', 'w') as f:
            import json
            json.dump(self.quotes_data, f, indent=4)
        self.log("Quotes saved to quotes_data.json")


################################NETWORKING DATA EXTRACTION FROM HERE R#############
#####ha code below will append the new data on the csv file net data 
###################################################################################################
class NetworkingSpider3(scrapy.Spider):
    name = "complete"
    
    # Default starting URL
    default_url = 'https://www.dmce.ac.in/'  # You can keep this as a default URL if you want

    custom_settings = {
        'FEEDS': {
            'C://EchoSift//data//net_data.csv': {
                'format': 'csv',
                'fields': ['URL', 'Status Code', 'Response Time (s)', 'Depth', 'IP Address', 'Request Headers', 'Response Headers', 'Content Length', 'User Agent', 'Redirected URLs', 'Encoding', 'Cookies'],
            },
        }
    }

    def __init__(self, url=None, *args, **kwargs):
        """
        Initialize the spider with a starting URL.
        
        :param url: The URL to scrape, passed as a parameter.
        """
        super().__init__(*args, **kwargs)
        
        # Set the start URL based on the provided URL or use the default
        self.start_urls = [url] if url else [self.default_url]

        # Check if the CSV file exists, if not, create it and write headers
        try:
            with open('C://EchoSift//data//net_data.csv', mode='r', encoding='utf-8') as file:
                pass  # File exists, do nothing
        except FileNotFoundError:
            # If file does not exist, create it and write headers
            with open('C://EchoSift//data//net_data.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['URL', 'Status Code', 'Response Time (s)', 'Depth', 'IP Address', 'Request Headers', 'Response Headers', 'Content Length', 'User Agent', 'Redirected URLs', 'Encoding', 'Cookies'])

    def parse(self, response):
        # Networking data
        url = response.url
        status_code = response.status
        response_time = response.meta.get('download_latency', 'N/A')  # Time taken to get the response
        depth = response.meta.get('depth', 0)  # Depth of the request
        ip_address = response.ip_address  # IP address of the server
        request_headers = response.request.headers.to_unicode_dict()  # Request headers
        response_headers = response.headers.to_unicode_dict()  # Response headers
        content_length = len(response.body)  # Content length of the response
        user_agent = response.request.headers.get('User-Agent', 'N/A').decode('utf-8')  # User-Agent
        redirected_urls = response.meta.get('redirect_urls', [])  # Any redirected URLs
        encoding = response.encoding if response.encoding else 'N/A'  # Response encoding
        cookies = response.headers.getlist('Set-Cookie')  # Cookies set by the server

        # Write networking data and extracted content to the CSV (appending new rows)
        with open('C://EchoSift//data//net_data.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([url, status_code, response_time, depth, ip_address, request_headers, response_headers, content_length, user_agent, ', '.join(redirected_urls), encoding, cookies])

        # Follow pagination links or further URLs if needed
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)


import scrapy
import scrapy

class CywareSpider(scrapy.Spider):
    name = 'cyware'
    start_urls = ['https://social.cyware.com/cyber-security-news-articles']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cyware_data = []  # Variable to store scraped data

    def parse(self, response):
        # Extract the title, information, and threat type
        titles = response.css('.cy-card__title::text').getall()
        descriptions = response.css('.cy-card__description::text').getall()
        threat_types = response.css('.cursor-pointer.d-block.text-decoration-none.text-bold.text-primary::text').getall()

        # Zip the data and store in the list
        for title, description, threat_type in zip(titles, descriptions, threat_types):
            self.cyware_data.append({
                'title': title.strip(),
                'description': description.strip(),
                'threat_type': threat_type.strip(),
            })

        # Debug: Print to ensure data is captured
        self.log(f"Captured Cyware data: {self.cyware_data}")

        # Follow pagination if available
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def closed(self, reason):
        # Save data to a JSON file after the spider finishes
        with open('cyware_data.json', 'w') as f:
            import json
            json.dump(self.cyware_data, f, indent=4)
        self.log("Cyware data saved to cyware_data.json")

import json 
import scrapy
import json

class NciipcSpider(scrapy.Spider):
    name = "nciipc"
    start_urls = ["https://nciipc.gov.in/alert_and_Advisories.html"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nciipc_data = []  # Variable to store scraped data

    def parse(self, response):
        # Extracting titles with links
        titles = response.css('.confirmation')
        
        for title in titles:
            title_text = title.css('b::text').get()  # Extract title text (inside <b>)
            title_link = title.css('a::attr(href)').get()  # Extract link from <a> tag

            # Extracting the entire content inside <font class="advisoryFont">
            advisory_font_content = title.xpath('following-sibling::p/font[@class="advisoryFont"]//text()').getall()
            description_text = ''.join(advisory_font_content).strip()

            # Extracting severity (CVE ID) which is inside the <b> tag within the advisoryFont class
            severity = title.xpath('following-sibling::p/font[@class="advisoryFont"]/b/text()').get()

            self.nciipc_data.append({
                'title': title_text.strip() if title_text else None,
                'link': response.urljoin(title_link) if title_link else None,
                'description': description_text if description_text else None,
                'severity': severity.strip() if severity else None
            })

        # Saving data to JSON
        with open('nciipc_data.json', 'w') as f:
            json.dump(self.nciipc_data, f, indent=4)

        # Logging success
        self.log(f"Data saved to nciipc_data.json")

class ThreatPostSpider(scrapy.Spider):
    name = 'threatpost'
    allowed_domains = ['threatpost.com']
    start_urls = ['https://threatpost.com/']

    def parse(self, response):
        articles = response.xpath('//article')
        for article in articles:
            yield {
                'title': article.xpath('.//h2/a/text()').get(),
                'description': article.xpath('.//div[@class="excerpt"]/text()').get(),
                'url': article.xpath('.//h2/a/@href').get()
            }

        next_page = response.xpath('//a[@class="next page-numbers"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


class CertSpider(scrapy.Spider):
    name = 'cert'
    allowed_domains = ['cert-in.org.in']
    start_urls = ['https://www.cert-in.org.in/']

    def parse(self, response):
        # Example: Extracting all text from paragraphs and headings
        for paragraph in response.xpath('//p/text()').getall():
            yield {'text': paragraph.strip()}

        for heading in response.xpath('//h3/text()').getall():
            yield {'heading': heading.strip()}

        # Follow pagination links if applicable (update selector as needed)
        next_page = response.xpath('//a[contains(text(), "Next")]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)            

class Rapid7Spider(scrapy.Spider):
    name = 'rapid7'
    start_urls = ['https://www.rapid7.com/db/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rapid7_data = []  # Variable to store scraped data

    def parse(self, response):
        # Extracting titles
        titles = response.css('.resultblock__info-title::text').getall()

        # Extracting dates and severity (stored together in .resultblock__info-meta)
        meta_data = response.css('.resultblock__info-meta::text').getall()

        # Pair the data and append to rapid7_data
        for title, meta in zip(titles, meta_data):
            meta = meta.strip().split(' | ')
            date = meta[0] if len(meta) > 0 else None
            severity = meta[1] if len(meta) > 1 else None

            self.rapid7_data.append({
                'title': title.strip() if title else None,
                'date': date.strip() if date else None,
                'severity': severity.strip() if severity else None,
            })

        # Debug: Log captured data
        self.log(f"Captured Rapid7 data: {self.rapid7_data}")

        # Follow pagination
        next_page = response.css('.pagination__next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            # Save the data when no more pages are left
            with open('rapid7_data.json', 'w') as f:
                json.dump(self.rapid7_data, f, indent=4)
            self.log("Data saved to rapid7_data.json")