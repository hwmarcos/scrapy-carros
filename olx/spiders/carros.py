# -*- coding: utf-8 -*-
import scrapy


class CarrosSpider(scrapy.Spider):
    name = 'carros'
    # allowed_domains = ['pe.olx.com.br/veiculos-e-pecas/carros']
    start_urls = ['http://sp.olx.com.br/veiculos-e-pecas/carros/']

    def parse(self, response):
        itens = response.xpath(
            # '//ul[@id="main-ad-list"]/li[contains(@class, "item") and not(contains(@class, "list_native"))]'
            '//ul[@id="main-ad-list"]/li[not(contains(@class, "list_native"))]'
        )
        self.log(len(itens))
        # pegando todos os itens da primeira página
        for item in itens:
            url = item.xpath('./a/@href').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_detail)
        # após verificar todos os itens da página, verifica se existe uma próxima página
        # next_page = response.xpath(
        #     '//div[contains(@class, "module_pagination")]//a[@rel = "next"]/@href'
        # )
        # if (next_page):
        #     np = next_page.extract_first()
        #     if (np <= 3):
        #         self.log('Próxima Página: {} '.format(np))
        #         yield scrapy.Request(url=np, callback=self.parse)

    def parse_detail(self, response):
        title = response.xpath('//title/text()').extract_first()
        year = response.xpath("//span[contains(text(), 'Ano')]/following-sibling::strong/a/@title").extract_first()
        ports = response.xpath("//span[contains(text(), 'Portas')]/following-sibling::strong/text()").extract_first()
        # fuel = response.xpath("//span[contains(text(), 'Combustível')]/following-sibling::strong/a/text()").extract_first()

        yield {
            'title': title,
            'year': year,
            'ports': ports
        }
