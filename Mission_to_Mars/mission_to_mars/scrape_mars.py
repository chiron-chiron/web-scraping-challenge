# Dependencies
from bs4 import BeautifulSoup
import requests
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from splinter import Browser
import pandas as pd


### NASA Mars News ###


executable_path = {'executable_path': ChromeDriverManager().install()}



def scrape():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # URL of page to be scraped
    url_nasa_mars_news = 'https://mars.nasa.gov/news/'
        # Tried using link provided, couldn't get it to work. 
        # Was advised by classmate, to use above link.
        # Was later advised by AskBSC redplanetscience was correct link.
        # Will use links provided in readme, moving forward.
    browser.visit(url_nasa_mars_news)
    
    # Retrieve page, with requests module
    response_mars = requests.get(url_nasa_mars_news)

    # Create BeautifulSoup object; parse with 'html.parser'
    news_soup = BeautifulSoup(response_mars.text, 'html.parser')
    # print(soup.prettify())

    # Find all div elements and class, for news titles
    news_titles = news_soup.find_all('div', class_="slide")
    
    for titles in news_titles:
        try:
            # Retrieve latest news title
            news_title = titles[0].find('div', class_='content_title').text.strip()
            # news_title = latest_title.text.strip()
            
            # Retrieve corresponding latest news paragraph
            news_p = news_titles[0].find('div', class_='rollover_description_inner').text.strip()
            # news_p = latest_paragrapph.text.strip()
        except AttributeError as AE
            print(AE)



    ### JPL Mars Space Images - Featured Image ###

    ## 1) open URL via splinter to navigate to url
    ## 2) use beautiful soup to parse page and obtain full size image .jpg
    ## 3) use splinter to navigate by clicking full image

    ## 1) open URL via splinter in prep to navigate to full image =========================
    # Import splinter and set up the chromedriver path
    # from splinter import Browser

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Set url
    mars_space_images_url = 'https://spaceimages-mars.com'

    # Use splinter to visit url
    browser.visit(mars_space_images_url)

    # Setup BeautifulSoup
    html = browser.html
    fullimage_html = BeautifulSoup(html, "html.parser")

    # Find link to full image page
    fullimage_url_link = fullimage_html.find('img', class_='headerimage fade-in').get('src')
    featured_image_url = (f'{mars_space_images_url}/{fullimage_url_link}')
    
    ## 3) use splinter to navigate by clicking full image ==================================
    # This was not required, as above link works to provide full image.
    # button_by_text = browser.find_by_text(' FULL IMAGE')
    # button_by_text.click()

    ## 4) Quit browser
    browser.quit()



    ### Mars Facts ###

    url_mars_facts = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url_mars_facts)
    # print(tables)

    # From type(tables), understand tables returned as list.append
    # Want 2nd table:
    mars_facts_df = tables[1]
    # mars_facts_df.head()

    # Rename columns
    mars_facts_df.columns = ["Profile_component", "Value"]
    mars_facts_df

    # Convert df to HTML table string, using pandas
    mars_facts_html = mars_facts_df.to_html
    # mars_facts_html



    ### Mars Hemispheres ###

    # def mars_hemispheres(browser):
        
    # executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url_hemis = 'https://marshemispheres.com/'
    browser.visit(url_hemis)


    ## Identify the full resolution links for all pictures
    # 1) Setup BeautifulSoup
    html_hemi = browser.html
    soup_hemi = BeautifulSoup(html_hemi, "html.parser")

    # Search on description, as this is unique to the 4 pictures/links.
    images = soup_hemi.find_all('div', class_="description")

    # To capture each iteration
    hemi_dict = {}

    # To append into dictionary
    hemisphere_image_url = []

    ## 2) Iterate through each link from base url:
    for image in images:
        # Scrape titles of each photo
        title = image.find('h3').text
        # print(title)
        
        # Obtain url link for image
        url_hemi_images = image.find('a')['href']
        # Construct full link to 
        img_url_ind = f'{url_hemis}{url_hemi_images}'
        # print(img_url_ind)    
        
        # Setup splinter in each individual hemi page
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser_hemis_ind = Browser('chrome', **executable_path, headless=True)
        browser_hemis_ind.visit(img_url_ind)
        
        # Setup BS
        html_img_ind = browser_hemis_ind.html
        soup_img_ind = BeautifulSoup(html_img_ind, "html.parser")
        
        # Now find full image URL from this page
        image_url_ind = soup_img_ind.find_all('img', class_="wide-image")
        url_ind = image_url_ind[0]['src']
        
        # Create full image url with base url
        img_url = f'{url_hemis}{url_ind}'
        # print(img_url)
        
        # Add title to dictionary
        hemi_dict = {"title": title, "img_url": img_url}
        
        # Append each interation so not overwritten
        hemisphere_image_url.append(hemi_dict)

    mars_data = []

    mars_data = {
            'news_title_latest': news_title,
            'news_para': news_p,
            'featured_image_url': featured_image_url,
            'mars_facts_df': mars_facts_df,
            'mars_facts': mars_facts_html,
            'hemisphere_image_url': hemisphere_image_url,
        }

    return mars_data
    