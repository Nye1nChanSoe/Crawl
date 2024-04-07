import requests as req
from bs4 import BeautifulSoup
import re
import time

url = 'https://www.shwerooms.com/'

start_time = time.time()  # Start time

response = req.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Save post boxes to a file
    with open('page1.txt', 'w') as f:
        post_boxes = soup.find_all(class_='post_box')
        total_count = len(post_boxes) 
        for post_box in post_boxes:
            # Remove HTML tags
            text_content = re.sub(r'<.*?>', '', str(post_box), flags=re.DOTALL)  
            # Strip leading and trailing whitespace
            text_content = text_content.strip()  
            # Replace multiple newlines with a single newline
            text_content = re.sub(r'\n+', '\n', text_content)  
            # Write text content to file with a new line after each div
            f.write(text_content + '\n\n\n\n')  

    end_time = time.time()
    time_taken = end_time - start_time

    # Add metadata at the top of the output files
    with open('page1.txt', 'r+') as f:
        content = f.read()
        f.seek(0, 0)  
        f.write(f'Website: {url}\nTotal count: {total_count}\nTime taken: {time_taken:.2f} seconds\n\n' + content)

    print('Results saved successfully.')

else:
    print('Failed to retrieve the web page')
