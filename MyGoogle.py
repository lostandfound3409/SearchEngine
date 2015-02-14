from google import search


class MyGoogle:

    def searchMe(self, searchQuery):
        url_list = []
        for url in search(searchQuery, tld='com', lang='en', num=10, start=0, stop=10, pause=2.0):
            url_list.append(url)
            if len(url_list) == 10:
                return url_list