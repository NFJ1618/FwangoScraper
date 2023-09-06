import requests

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        
        return response.text  # Return the content of the page
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    url = "https://fwango.io/togramdslam2023"
    page_content = fetch_page(url)
    if page_content:
        print(page_content)  # You can then parse the page content as needed
