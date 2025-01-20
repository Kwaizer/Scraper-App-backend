class JobPosting:
    def __init__(self, title, link, description, pub_date, guid, categories):
        self.title = title
        self.link = link
        self.description = description
        self.pub_date = pub_date
        self.guid = guid
        self.categories = categories

    def __str__(self):
        return f"Title: {self.title}\n" \
               f"Link: {self.link}\n" \
               f"Description: {self.description}\n" \
               f"Published Date: {self.pub_date}\n" \
               f"GUID: {self.guid}\n" \
               f"Categories: {self.categories}\n" \
               f"----------------------------------"
    
    def to_dict(self):
        return {
            "title": self.title,
            "link": self.link,
            "description": self.description,
            "pub_date": self.pub_date,
            "guid": self.guid,
            "categories": self.categories,
        }
