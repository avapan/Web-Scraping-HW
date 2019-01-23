from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:\Users\kikip\Desktop\chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

#Create dictionary
mars_info = {}

#Nasa News
def scrape_mars_news():
    try:
    
        #Initialize browser
        browser = init_browser()

        # Visit NASA
        url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
        browser.visit(url)

        time.sleep(1)

        # Scrape page into Soup
        html = browser.html
        soup = bs(html, "html.parser")

        # Get news title and news_paragraph
        news_title = soup.find('div',class_='content_title').text
        news_p = soup.find('div', class_='article_teaser_body').text

        # Store data in a dictionary
        mars_info['news_title'] = news_title
        mars_info['news_paragragh'] = news_p

        # Return results
        return mars_info

    finally:
        browser.quit()

#Featured Image
def scrape_mars_image():
    try:

        #Initialize Browser
        browser = init_browser()

        #Visit Mars Image
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        
        browser.click_link_by_partial_text('FULL IMAGE')
        time.sleep(2)
        browser.click_link_by_partial_text('more info')
        time.sleep(2)
        browser.click_link_by_partial_text('.jpg')

        #scrape image into soup
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        featured_img_url = soup.find('img').get('src')

        featured_img_url
        
        mars_info['featured_img_url']=featured_img_url
        
        return mars_info

    finally:

        browser.quit()

# Mars Weather
def scrape_mars_weather():

    try:
        # Initialize browser
        browser = init_browser()

        # Visit Mars Weather
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        #Scrape weather into soup
        weather_html = browser.html
        soup = BeautifulSoup(weather_html, "html.parser")
        mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
        mars_weather

        mars_info['mars_weather']= mars_weather

        return mars_info

    finally:
        browser.quit()

def scrape_mars_facts():
    facts_url = 'https://space-facts.com/mars/'
    facts_df = pd.read_html(facts_url)[0]
    facts_df = facts_df.rename(columns={0:'Description', 1:''})
    facts_df = facts_df.set_index('Description', drop=True)
    facts_html = facts_df.to_html(classes = 'table table-striped')

    mars_info['mars_facts']=facts_html

    return mars_info

def scrape_mars_hemisphere():

    try:
        browser = init_browser()
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        html_hemispheres = browser.html
        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        hemisphere_image_urls = []

        hemisphere_dict = {'title': [], 'img_url': [],}

        x = soup.find_all('h3')


        for i in x:
            t = i.get_text()
            title = t.strip('Enhanced')
            browser.click_link_by_partial_text(t)
            url = browser.find_link_by_partial_href('download')['href']
            hemisphere_dict = {'title': title, 'img_url': url}
            hemisphere_image_urls.append(hemisphere_dict)
        
        mars_info['mars_hemisphere'] = hemisphere_image_urls

        return mars_info
    finally:
        browser.quit()