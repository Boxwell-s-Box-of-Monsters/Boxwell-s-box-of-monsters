import json
import unittest
from urllib.request import urlopen

class TestImageUrls(unittest.TestCase):

    # Test to make sure no image urls are bad
    def testImageUrls(self):
        brokenUrls = []
        with open('./json/data.json', "r") as file:
            documents = json.load(file)
            for document in documents:
                imageUrl = document["imageURL"]
                try:
                    urlopen(imageUrl)
                except Exception as e:
                    brokenUrls.append({document["name"]: imageUrl})
        print(brokenUrls)
        self.assertEqual(len(brokenUrls), 0)

if __name__ == "__main__":
    unittest.main()
        