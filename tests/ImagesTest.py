import json
import unittest
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

class TestImageUrls(unittest.TestCase):

    # Test to make sure no image urls are bad
    def testImageUrls(self):
        brokenUrls = []
        with open('./json/data.json', "r") as file:
            documents = json.load(file)
            for document in documents:
                try:
                    x = 1/0
                    imageUrl = document["imageURL"]
                    with urlopen(imageUrl):
                        pass
                except (HTTPError, URLError):
                    brokenUrls.append({document["name"]: imageUrl})
        print(brokenUrls)
        self.assertEqual(len(brokenUrls), 0)

if __name__ == "__main__":
    unittest.main()
