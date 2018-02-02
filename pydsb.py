import bs4
import requests


class PyDSB:
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.entries = self.get_entries()


    def _data_from_api(self):
        """Get data from API"""
        # Login and fetch token id
        login_request = requests.get("https://iphone.dsbcontrol.de/iPhoneService.svc/DSB/authid/" + self.username + "/" + self.password)
        login_token_id = login_request.text

        # If wrong password or username
        if login_token_id == "\"00000000-0000-0000-0000-000000000000\"":
            raise LoginError("Username or password is wrong")

        # Get data from API
        data_request = requests.get("https://iphone.dsbcontrol.de/iPhoneService.svc/DSB/timetables/" + login_token_id.replace("\"", ""))
        data = data_request.json()

        # Create list with timetables
        timetables = [timetable["timetableurl"] for timetable in data]

        return timetables


    def get_entries(self):
        """Parse entries"""
        # Get data from API
        timetables = self._data_from_api()

        # Initialize list for final entries
        results = []

        for timetable in timetables:
            # Init beautiful soup
            sauce = requests.get(timetable).text
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

                # Replace ? with "instead"
                if "?" in infos[2].text:
                    infos_subject = infos[2].text.split("?")[1] + " statt " + infos[2].text.split("?")[0]
                else:
                    infos_subject = infos[2].text

                # Replace ? with "instead"
                if "?" in infos[3].text:
                    infos_room = infos[3].text.split("?")[1] + " statt " + infos[3].text.split("?")[0]
                else:
                    infos_room = infos[3].text

                # If entry contains several classes (10cG, 10dG)
                for class_ in infos[0].text.split(", "):
                    # Create new dictionary with information
                    new_entry = {
                        "class": class_,
                        "period": infos[1].text,
                        "subject": infos_subject,
                        "room": infos_room,
                        "type": infos[4].text,
                        "text": infos[5].text,
                        "date": date,
                        "day": day
                    }

                    # Add result to list
                    results.append(new_entry)

        return results


    def get_messages(self):
        """Parse messages"""
        # Get data from API
        timetables = self._data_from_api()

        # Initialize list for final entries
        results = []

        for timetable in timetables:

            # Init beautiful soup
            sauce = requests.get(timetable).text
            soup = bs4.BeautifulSoup(sauce, "html.parser")

            # Get date and day
            date = soup.find("div", class_="mon_title").text.split(" ")[0]
            day = soup.find("div", class_="mon_title").text.split(" ")[1]

            # Find table with information
            table = soup.find("table", class_="info")

            if table:

                messages = table.find_all("tr", class_="info")
                # Remove first entry, because it's the table header
                messages.pop(0)

                for i in messages:
                    # Get columns of one message and remove special characters
                    message_columns = [" ".join(column.text.split()) for column in i.find_all("td")]

                    # Join columns
                    message = ": ".join(message_columns)

                    message = {
                        "date": date,
                        "day": day,
                        "message": message
                    }

                    # Add result to list
                    results.append(message)

        return results


class LoginError(Exception):
    pass

