import urlparse
import scrapy

from scrapy.http import Request

class photo_motion(scrapy.Spider):
    name = "photoThumbs"

    allowed_domains = [open('conf','r').read().strip()]
    event_url = allowed_domains[0] + "/groupSessionSelection.php?mode=listSessions&groupID=&eventID="
    start_urls = []
    for eventID in range(6,17):
	start_urls.append( event_url + str(eventID) )

    def parse(self, response):
	print response.css('div a::attr(href)').extract()[1:-1]
#	    yield Request(
#		url=response.url.join(href),
#		callback=self.parse_race
#	    )

    def parse_race(self, response):
#	for href in response.css('div.download_wrapper a[href$=".img"]::attr(href)').extract():
	    print href
            yield Request(
                url=response.urljoin(href),
                callback=self.save_img
            )

    def save_img(self, response, groupID):
        path = response.url.split('/')[-1]
        self.logger.info('Saving IMG %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)
