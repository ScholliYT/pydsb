import base64
import bs4
import gzip
import json
import requests
import time


class QueryDays:
    TODAY = "tod"
    TOMORROW = "tom"
    DAYAFTERTOMORROW = "dat"


class PyDSB:
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.entries = self.get_entries()


    def data_from_api(self):
        """Get data from API"""
        # Official API with data
        url = "https://www.dsbmobile.de/JsonHandlerWeb.ashx/GetData"

        # Arguments for request
        arguments = {
            "UserId": self.username,
            "UserPw": self.password,
            "Abos": [],
            "AppVersion": "2.3",  # Update to 2.3
            "Language": "de",
            "OsVersion": "",
            "AppId": "",
            "Device": "WebApp",
            "PushId": "",
            "BundleId": "de.heinekingmedia.inhouse.dsbmobile.web",
            "Date": time.strftime("%a %b %m %Y %H:%M:%S +0000"),
            "LastUpdate": time.strftime("%a %b %m %Y %H:%M:%S +0000")
        }

        # JSON encode
        arguments_json = json.dumps(arguments, ensure_ascii=False).encode("utf-8")

        # GZIP encode
        arguments_gzip = gzip.compress(arguments_json)

        # Base64 encode
        arguments_base64 = base64.b64encode(arguments_gzip)

        # Create JSON data
        data = {
            "req": {
                "Data": str(arguments_base64, "utf-8"),
                "DataType": 1,
            }
        }

        # Define HTTP headers
        headers = {
            "Bundle_ID": "de.heinekingmedia.inhouse.dsbmobile.web",
            "Content-Type": "application/json;charset=utf-8"
        }

        # POST-Request to API
        r = requests.post(url, data=str(data), headers=headers)

        # Read data from API
        data = r.json()["d"]

        # Decode Base64
        data_base64 = base64.b64decode(data)

        # Decode GZIP
        data_uncompressed = gzip.decompress(data_base64)

        # Convert data to JSON
        data_json = json.loads(str(data_uncompressed, "utf-8"))

        return data_json


    def get_entries(self):
        """Parse entries"""
        # Get raw JSON data from API
        data = self.data_from_api()

        # Get list with URLs from data
        pages = data["ResultMenuItems"][0]["Childs"][1]["Root"]["Childs"][0]["Childs"]

        # Initialize list for final entries
        results = []

        for page in pages:
            # URL for one page
            page_url = page["Detail"]

            # Init beautiful soup
            sauce = requests.get(page_url).text
            soup = bs4.BeautifulSoup(sauce, "html.parser")

            # Get date and day
            date = soup.find("div", class_="mon_title").text.split(" ")[0]
            day = soup.find("div", class_="mon_title").text.split(" ")[1]

            # Find table with information
            table = soup.find("table", class_="mon_list")
            entries = table.find_all("tr")

            # Remove first entry, because it's the table header
            entries.pop(0)

            # For every entry (entry = one line)
            for entry in entries:
                # Find every column
                infos = entry.find_all("td")

                # Create new dictionary with information
                new_entry = {
                    "class": infos[0].text,
                    "period": infos[1].text,
                    "subject": infos[2].text,
                    "room": infos[3].text,
                    "type": infos[4].text,
                    "text": infos[5].text,
                    "date": date,
                    "day": day
                }

                # Add result to list
                results.append(new_entry)

        return results

    def query_date(self, day=QueryDays.TODAY, month=QueryDays.TODAY, year=QueryDays.TODAY):
        # Use date of today if necessary
        if day == QueryDays.TODAY:
            day = int(time.strftime("%d"))
        if month == QueryDays.TODAY:
            month = int(time.strftime("%m"))
        if year == QueryDays.TODAY:
            year = int(time.strftime("%Y"))

        # Create empty list with results
        entries = []

        # Check every entry whether date is right
        for i in self.get_entries():
            entry_day = int(i["date"].split(".")[0])
            entry_month = int(i["date"].split(".")[1])
            entry_year = int(i["date"].split(".")[2])

            if day == entry_day and month == entry_month and year == entry_year:
                entries.append(i)

        return entries

    def query_class(self, class_):
        entries = [i for i in self.get_entries() if i["class"] == class_]
        return entries
