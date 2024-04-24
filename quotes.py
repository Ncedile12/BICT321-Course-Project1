import scrapy

class LinkedinJobsSpider(scapy.Spider):
    name = "Linkedin_jobs"
    api_url ='https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Python%2B%28Programming%2BLanguage%29&location=South%2BAfrica&geoId=104035573&trk=public_jobs_jobs-search-bar_search-submit&start=25'

def start_requests(self):
    first_job_on_page = 0
    first_url = self.api_url + str(first_job_on_page)
    yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page':first_job_on_page})

def parse_job(self_response):
    first_job_on_page = response.meta['irst_job_on_page']

    jobs = response.css("li")

    num_jobs_returned = len(jobs)
    print("******** Num Jobs Returned *********")
    print(num_jobs_returned)

    for job in jobs:
        job_item = {}

        job_item['job_title'] = job.css("h3::text").get(default='not-found').strip()
        job_item['job_detail_url'] = job.css(".base-card__full-link::attr(href)").get(default='not-found').strip()
        job_item['job_listed'] = job.css('time::text').get(default='not-found').strip()

        job_item['company_name'] = job.css("h4::text").get(default='not-found').strip()
        job_item['company_link'] = job.css(".base-card__full-link::attr(href)").get(default='not-found').strip()
        job_item['company_loaction'] = job.css('.job-search-card__location::text').get(default='not-found').strip()
        yield job_item


    if num_jobs_returned > 0:
       first_job_on_page = int(first_job_on_page) + 25
       next_url = self.api_url + str(first_job_on_page)
       yield scrapy.Request(url=next_url,  callback=self.parse_job, meta={'first_job_on_page':first_job_on_page})
