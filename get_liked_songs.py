import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
import time
import codecs
from tqdm import tqdm

PATH_TO_DRIVER = "chrome_driver/chromedriver.exe" # Path to the chrme driver
HEADLESS = True
USER = ""

def init():
    options = Options()
    options.headless = HEADLESS
    options.add_argument('log-level=3') 
    driver = webdriver.Chrome(PATH_TO_DRIVER, options=options)
    return driver

def main():
    driver = init()
    
    
    url = f"https://soundcloud.com/{USER}/"
    #load user's profile page to get the number of liked songs 
    driver.get(url)
    # get the number of liked songs
    liked = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div[4]/div[2]/div/article[3]/a/h3/span[2]").text
    num_likes = int(liked.split(" ")[0].replace(",",""))
    
    print(f"found {num_likes} songs\n")
    
    #load the user's liked page
    driver.get(url+"likes")
    time.sleep(1)
    songs = driver.find_elements(By.CLASS_NAME , "soundList__item")
    #val = songs[0].find_element(By.CLASS_NAME, "soundTitle__usernameText").text;
    #print(val)
    #val = songs[0].find_element(By.XPATH, '//*[@id="content"]/div/div/div[2]/div/div[2]/ul/li[1]/div/div').text;
    #val = songs[0].find_element_by_css_selector('span').get_attribute("aria-label");

    progress_bar = tqdm(total=num_likes)
    progress_bar.update(len(songs))
    prev_val = len(songs)
    while len(songs) < num_likes:
        scroll_height = driver.execute_script("return document.body.scrollHeight;")   
        driver.execute_script(f"window.scrollTo(0, {scroll_height});")
        time.sleep(0.5)
        songs = driver.find_elements(By.CLASS_NAME , "soundList__item")
        progress_bar.update(len(songs)-prev_val)
        prev_val = len(songs)
    progress_bar.close()
    
    with codecs.open("song_list.txt", "w", "utf-8-sig") as file:          
        for i,song in enumerate(songs):
            song_creator = song.find_element(By.CLASS_NAME, "soundTitle__usernameText").text;
            song_name = song.find_element(By.CSS_SELECTOR, 'span').get_attribute("aria-label");
            song_name = song_name
            #print(f"No.{i+1} Creator: {song_creator}, Song name: {song_name}")
            file.write(f"Creator: {song_creator}, Song name: {song_name}\n")
            
    
if __name__ == "__main__":
    main()