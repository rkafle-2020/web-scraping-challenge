# Import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time 
import requests
import pandas as pd

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Assign URL and visit with browser
    url= "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(1)

    # Create an HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    # Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. Assign the text to variables.
    news_title = soup.find_all("div", class_="content_title")[1].text

    # Find and print first paragraph
    news_p = soup.find("div", class_="article_teaser_body").text
    time.sleep(1)

    # Load URL for image and visit using splinter 
    image_url= "https://www.jpl.nasa.gov/images?search=&category=Mars"
    browser.visit(image_url)

    # Find the latest featured image using splinter and click on it
    time.sleep(1)
    browser.find_by_css('.mb-3').click()
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Locate image using splinter, assign to a variable, and save and print complete URL
    featured_img= soup.find("img", class_="BaseImage")
    featured_img_url= featured_img['data-src']
    time.sleep(1)

 ### Mars Facts
     # Visit the Mars Facts webpage (https://space-facts.com/mars/) and assign to variable name
    facts_url= "https://space-facts.com/mars/"
    browser.visit(facts_url)  

    # Read table on webpage using Pandas and assign to variable name
    mars_table=pd.read_html(facts_url)

    # Create dataframe using scraped data
    facts_df = mars_table[0]

    # Rename columns and set 'Category' column as index
    facts_df.columns= (['Category', 'Mars Facts'])
    mars_table_clean=facts_df.drop(0)
    clean_df=mars_table_clean.set_index('Category')

    # Use Pandas to convert the data to a HTML table string to use in Mongo dictionary.
    html_table_mongo = clean_df.to_html()

### Mars Hemispheres
    # Visit the USGS Astrogeology site
    astrogeo_url= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(astrogeo_url)

    # Create an HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Scrape the USGS Astrogeology site and collect high resolution images for each of Mar's hemispheres. 
    # Save both the image url string for the full resolution hemisphere image and the Hemisphere title containing the hemisphere name. 

    # Starting with first hemisphere listed, click on hemisphere name
    cerb_url=browser.links.find_by_partial_text('Cerberus')
    cerb_url.click()

    # Sleep browser for one second and create a new HTML object on page
    time.sleep(1)
    html = browser.html
    # Parse Cerberus page HTML with Beautiful Soup
    soup_cerb = bs(html, 'html.parser')

    # Using BeautifulSoup, locate and save hemisphere image and title 
    cerb_photo = soup_cerb.find("a", text="Sample").get("href")
    cerb_title = soup_cerb.find("h2", class_="title").text
    browser.back()
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    schia_url=browser.links.find_by_partial_text('Schiaparelli')
    schia_url.click()

    time.sleep(1)
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup_schia = bs(html, 'html.parser')
    schia_photo = soup_schia.find("a", text="Sample").get("href")
    schia_title = soup_schia.find("h2", class_="title").text
    browser.back()

    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    syrtis_url=browser.links.find_by_partial_text('Syrtis')
    syrtis_url.click()
    time.sleep(1)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup_syrtis = bs(html, 'html.parser')
    syrtis_photo = soup_syrtis.find("a", text="Sample").get("href")
    syrtis_title = soup_syrtis.find("h2", class_="title").text
   
    browser.back()
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    valles_url=browser.links.find_by_partial_text('Valles')
    valles_url.click()
    time.sleep(1)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup_valles = bs(html, 'html.parser')
    valles_photo = soup_valles.find("a", text="Sample").get("href")
    valles_title = soup_valles.find("h2", class_="title").text
    browser.back()

# Store hemisphere images in a list of dictionaries
    hemisphere_image_urls=[
        {"title": cerb_title, "img_url": cerb_photo},
        {"title": schia_title, "img_url": schia_photo},
        {"title": syrtis_title, "img_url": syrtis_photo},
        {"title": valles_title, "img_url": valles_photo}
]

#Store table and headlines in dictionary
    mars_facts= {
        'Headline': news_title,
        'News': news_p,
        'Featured_Image': featured_img_url,
        'Table': html_table_mongo,
        'Hemisphere_Images': hemisphere_image_urls
    }
    return mars_facts

    browser.quit()
# Return results
        
