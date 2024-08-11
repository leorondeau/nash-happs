import requests
from bs4 import BeautifulSoup

def scrape_calendar(url):
    # Send HTTP request to fetch the webpage
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the calendar container or specific elements containing event data
        calendar_container = soup.find('div', class_='calendar-container')
        if calendar_container:
            # Extract event data from the calendar container
            events = []
            for event in calendar_container.find_all('div', class_='event'):
                event_date = event.find('span', class_='date').text.strip()
                event_title = event.find('h3', class_='title').text.strip()
                event_description = event.find('p', class_='description').text.strip()
                events.append({
                    'date': event_date,
                    'title': event_title,
                    'description': event_description
                })
            return events
        else:
            print("Calendar container not found")
    else:
        print("Failed to fetch webpage")

# Example usage
url = 'https://localnash.com/calendar/'
events = scrape_calendar(url)
if events:
    for event in events:
        print(event)
