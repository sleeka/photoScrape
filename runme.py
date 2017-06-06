import urlparse
import scrapy

from scrapy.http import Request

class photo_motion(scrapy.Spider):
    name = "photoThumbs"

    allowed_domains = []
    with open('conf','r') as f:
	allowed_domains.append(f.read().strip())

    event_url = "http://" + allowed_domains[0] + "/groupSessionSelection.php?mode=listSessions&groupID=&eventID="

    start_urls = []
    for eventID in range(6,7):
	start_urls.append( event_url + str(eventID) )

    def parse(self, response):
	for href in response.css('div a::attr(href)').extract()[1:-1]:
	    yield Request(
		url = "http://" + self.allowed_domains[0] + href,
		callback = self.parse_race
	    )

    def parse_race(self, response):
	print response.xpath('img/@src').extract()
#	exit()
#	for href in response.css('div.download_wrapper a[href$=".img"]::attr(href)').extract():
#	    print href
 #           yield Request(
  #              url=response.urljoin(href),
   #             callback=self.save_img
    #        )

    def save_img(self, response, groupID):
        path = response.url.split('/')[-1]
        self.logger.info('Saving IMG %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)
