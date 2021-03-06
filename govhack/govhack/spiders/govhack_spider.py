import scrapy

from govhack.items import GovhackItem

banned = [
"best innovative hack utilising Statistics NZ data",
"How can we better understand how councils are performing?",
"How can we reduce the incidence of dog attacks? / How can we ensure that New Zealanders are excellent dog owners?",
"Melbourne's Ecology",
"Showcase Whanganui",
"Western Australian Entrepeneurial Prize",
"Western Australian Solution Prize",
"Whanganui community hack"
]

class GovhackSpider(scrapy.Spider):
    name = 'govhack'
    allowed_domains = ['2016.hackerspace.govhack.org']
    start_urls = [
        "https://2016.hackerspace.govhack.org/projects/"
    ]
    
    def parse(self, response):
        item = GovhackItem()
        regions = response.xpath('//table/tbody/tr/td[@class="views-field views-field-field-region"]/a/text()').extract()
        local_events = response.xpath('//table/tbody/tr/td[@class="views-field views-field-field-event-location"]/a/text()').extract()
        project_names = response.xpath('//table/tbody/tr/td[@class="views-field views-field-title active"]/a/text()').extract()
        team_names = response.xpath('//table/tbody/tr/td[@class="views-field views-field-field-team-name"]/a/text()').extract()
        websites = response.xpath('//table/tbody/tr/td[@class="views-field views-field-title active"]/a[last()]/@href')
        i = 0
        for href in websites:
            item['region'] = regions[i]
            item['local_event'] = local_events[i]
            item['project_name'] = project_names[i]
            item['team_name'] = team_names[i]
            item['is_user']   = True
            url = response.urljoin(href.extract())
            item['website'] = url
            i += 1
            yield item
            yield scrapy.Request(url, callback=self.parse_dir_contents)
            
    def parse_dir_contents(self, response):
        item = GovhackItem() 
        item['is_user'] = False
        item['website'] = response.url
        item['prizes'] = filter(lambda p: p not in banned, response.xpath('//body/div/div/section/div/section/article/div[@class="field field-name-field-prizes field-type-entityreference field-label-above"]/div/div/a/text()').extract())
        yield item
            
