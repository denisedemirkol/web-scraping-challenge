from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse   import urljoin
import pandas as pd

def scrape():

    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    listings = {}

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # ******************************************************************************
    #PART I: Scrap latest news from NASA

    p_lates_title = soup.find('div',class_='content_title').string
    p_lates_text  = soup.find('div',class_='article_teaser_body').string


    # ******************************************************************************
    #PART II: JPL SPACE IMAGES

    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image_url = soup.find('img',class_='headerimage')
    full_featured_image_url = urljoin(image_url, featured_image_url['src'])

    # ******************************************************************************
    #PART III: MARS FACTS

    fact_url = 'https://galaxyfacts-mars.com/'

    fact_tables = pd.read_html(fact_url, header =0) 
    fact_df     = fact_tables[0]

    fact_df.set_index(fact_df.columns[0], drop=True, append=False, inplace=True, verify_integrity=False)
    fact_df.index.name = None

    fact_html   = fact_df.to_html()        

    # ******************************************************************************
    #PART IV: MARS HEMISPHERE PHOTOS


    mars_url = 'https://marshemispheres.com/'
    browser.visit(mars_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_urls_dict = []

    images_list = soup.find_all('div',class_='item')

    for items in images_list:
        title   = items.text.strip()
        sub_url = urljoin(mars_url, items.find('a')['href'])
        browser.visit(sub_url)

        html2 = browser.html
        soup2 = BeautifulSoup(html2, 'html.parser')
        
        sub_title = soup2.find('h2').text.strip() 
        image_url = soup2.find('img',class_='wide-image')    
        full_image_url = urljoin(sub_url, image_url['src'])

        hemisphere_urls_dict.append({'title':sub_title, 'img_url':full_image_url})



    # Store data in a dictionary
    listings = {
        "featured_image_url": full_featured_image_url,
        "facts_table"       : fact_html,
        "hemisphere_urls"   : hemisphere_urls_dict,
        "latest_news_title" : p_lates_title,
        "latest_news_text"  : p_lates_text
    }


    # Quit the browser
    browser.quit()

    return listings
