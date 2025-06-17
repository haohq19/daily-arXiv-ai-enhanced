import re

class DailyArxivPipeline:
    def __init__(self):
        self.page_size = 100
        keywords = "event, dvs, neuromorphic"  # Default keywords, can be overridden by environment variable
        keywords = keywords.split(",")
        keywords = set(map(str.strip, keywords))   # keywords to filter papers, e.g.. {"event", "dvs", "neuromorphic"}
        self.keyword_pattern = re.compile('|'.join(map(re.escape, keywords)), re.IGNORECASE)
        print(keywords)
        print(bool(self.keyword_pattern.search('event-based cameras')))  # Example usage to ensure the pattern is compiled correctly
        print(bool(self.keyword_pattern.search('neuromorphic computing')))  # Example usage to ensure the pattern is compiled correctly
        print(bool(self.keyword_pattern.search('machine learning')))

    def check_keywords(self, text: str) -> bool:
        if not text:
            return False
        return bool(self.keyword_pattern.search(text))
    
    def process_item(self, item: dict):
        # item["pdf"] = f"https://arxiv.org/pdf/{item['id']}"
        # item["abs"] = f"https://arxiv.org/abs/{item['id']}"
        # item["authors"] = ["test"]
        # item["title"] = "test"
        # item["categories"] = "test"
        # item["comment"] = "test"
        # item["summary"] = "test event neuromorphic"
        # print(item)

        if (not self.check_keywords(item["summary"])) and (not self.check_keywords(item["title"])):
            print("error")
            return None
        print(f"Processed paper {item['id']} - {item['title']}")

        return item

if __name__ == "__main__":
    pipeline = DailyArxivPipeline()
    test_item = {
        "id": "123456",
        "summary": "This is a test summary about event-based cameras and neuromorphic computing.",
        "title": "Event-based Cameras: A New Frontier in Neuromorphic Computing",
        "authors": ["John Doe", "Jane Smith"],
        "categories": ["cs.CV", "cs.NE"],
        "comment": "This paper discusses the advancements in event-based cameras.",
    }
    pipeline.process_item(test_item)  # Simulating the spider argument as None