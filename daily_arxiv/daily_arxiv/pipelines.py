# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
import os
import arxiv
from scrapy.exceptions import DropItem

class DailyArxivPipeline:
    def __init__(self):
        self.page_size = 100
        self.client = arxiv.Client(self.page_size)
        keywords = os.environ.get("KEYWORDS", "cs.CV")
        keywords = keywords.split(",")
        keywords = set(map(str.strip, keywords))   # keywords to filter papers, e.g.. {"event", "dvs", "neuromorphic"}
        self.keyword_pattern = re.compile('|'.join(map(re.escape, keywords)), re.IGNORECASE)

    def check_keywords(self, text: str) -> bool:
        if not text:
            return False
        return bool(self.keyword_pattern.search(text))
    
    def process_item(self, item: dict, spider):
        item["pdf"] = f"https://arxiv.org/pdf/{item['id']}"
        item["abs"] = f"https://arxiv.org/abs/{item['id']}"
        search = arxiv.Search(
            id_list=[item["id"]],
        )
        paper = next(self.client.results(search))
        item["authors"] = [a.name for a in paper.authors]
        item["title"] = paper.title
        item["categories"] = paper.categories
        item["comment"] = paper.comment
        item["summary"] = paper.summary
        # print(item)

        if (not self.check_keywords(item["summary"])) and (not self.check_keywords(item["title"])):
            spider.logger.debug(f"Skipped paper {item['id']} - {item['title']}")
            raise DropItem(f"No keywords matched")

        spider.logger.info(f"Processed paper {item['id']} - {item['title']}")
        return item
