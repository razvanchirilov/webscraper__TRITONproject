# webscraper__TRITONproject

FIRST STEP
Install the packages specified in a requirements.txt. 

All you need to do is open your command prompt or terminal, navigate to the directory where the requirements.txt file is located, and type   ==>   pip install -r requirements.txt. 

This command will install all the packages listed in the file for you. It's a convenient way to ensure that all the required packages are installed before you run your project.

This project is a web scraping tool that extracts data from the Triton website related to vacuum cleaners and pressure washers. 
The tool uses the Scrapy framework and Scrapy-Splash to enable JavaScript rendering. 
The data is extracted from the Triton website and stored in a CSV and Excel files using the ScrapyPyXlsx library.

The VacuumCleanersSpider is the main spider that crawls the Triton website and extracts data from multiple pages. 
It starts by sending a request to each of the URLs specified in the start_urls list. 
The start_requests method sends a request using Scrapy-Splash, which allows JavaScript rendering. 
The parse method extracts data from the first page of each URL, including product title, price, availability, and link to the product page. 
It then sends a request to each product page to extract additional details, such as product code. 

Finally, the parse_product_page method uses an item loader to store the extracted data in a TritonprojectItem object, which is then saved in an Excel file using ScrapyPyXlsx.


The main driver section runs the spider by creating a CrawlerProcess and calling process.crawl(VacuumCleanersSpider) to start the spider. 
The process.start() method then runs the spider, which starts the scraping process.
