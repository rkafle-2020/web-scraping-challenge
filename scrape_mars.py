from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import time

def init_browser():
    executable_path = {'executable_path':'C:\Users\renuk\.wdm\drivers\chromedriver\win32\89.0.4389.23\chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=True)

def scrape():
    """ Scrapes all websites for Mars data """
    
    # URLs of pages to be scraped
    nasa_mars_news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #scrape news url
    nasa_mars_news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'


# Retrieve page with the requests module
    news_response = requests.get(nasa_mars_news_url)
# Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(news_response.text, 'html.parser')
# results are returned as an iterable list
    results = soup.find_all(class_="slide")
    titles_list = []
    paragraphs_list = []
# Loop through returned results
    for result in results:
   
        links = result.find_all('a')
        title = links[1].text
        paragraph = result.find(class_="rollover_description_inner").text
    #Append both to a list
        titles_list.append(title)
        paragraphs_list.append(paragraph)
    news_title = titles_list[0]
    news_p = paragraphs_list[0]

#Second Web Scrape for Mars Image

    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(featured_image_url)
    image_button= browser.find_by_css("button.btn.btn-outline-light")
    image_button.click()
    html=browser.html
# Create BeautifulSoup object; parse with 'html.parser'
    image_soup = BeautifulSoup(html, 'html.parser')
#get Featured Image link
    featured_image_link = image_soup.find("img", class_= "fancybox-image").get("src")

#featured image clean link
    featured_image = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{featured_image_link}"
   
       
#mars fact table
    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)
    mars_table= pd.read_html(mars_facts_url)[0]
    mars_table= mars_table.rename(columns={0:"Description",1:"Mars"})
    mars_table= mars_table.set_index("Description")
    mars_table.to_html()

#get the links for hemisphere images
    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(mars_hemisphere_url)
# Scrape astrogeology.usgs.gov for hemisphere image urls and titles
    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemisphere_url)

    hemisphere_html = browser.html
    hemisphere_soup = BeautifulSoup(hemisphere_html, 'lxml')
    base_url ="https://astrogeology.usgs.gov"

    image_list = hemisphere_soup.find_all('div', class_='item')

# Loop through each hemisphere and click on link to find large resolution image url
    for image in image_list:
        hemisphere_dict = {}
    
        href = image.find('a', class_='itemLink product-item')
        link = base_url + href['href']
        browser.visit(link)
    
        time.sleep(1)
    
        hemisphere_html2 = browser.html
        hemisphere_soup2 = BeautifulSoup(hemisphere_html2, 'lxml')
    
        img_title = hemisphere_soup2.find('div', class_='content').find('h2', class_='title').text
        hemisphere_dict['title'] = img_title
    
        img_url = hemisphere_soup2.find('div', class_='downloads').find('a')['href']
        hemisphere_dict['url_img'] = img_url
    
# Append dictionary to list
    hemisphere_image_urls.append(hemisphere_dict)

    scraped_dict = {
                'Featured Image': featured_image_link,
                'News Title': news_title,
                'News Body': news_p,
                'Mars Facts':mars_table,
                'Hemispheres': hemisphere_image_urls,
               }

    return (scraped_dict)