import requests
from bs4 import BeautifulSoup

def fetch_district_names(url_template, x_values, class_name):
    district_names = {}

    for x in x_values:
        url = url_template.format(x=x)
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            element = soup.find('div', class_=class_name)
            
            if element:
                district_names[x] = element.text.strip()
            else:
                district_names[x] = "Element not found"
        else:
            district_names[x] = "Failed to retrieve the page"

    return district_names

# Define the URL template and the range of x values
url_template = 'https://www.house.kg/snyat?region=1&town=2&district=4&child_district={x}&sort_by=upped_at+desc'
x_values = range(1, 10)  # Replace with the actual range of x values
class_name = 'filter-option-inner-inner'  # The class name for the target element

# Fetch district names
district_names = fetch_district_names(url_template, x_values, class_name)

# Print the resulting dictionary
print(district_names)
