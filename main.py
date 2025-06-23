from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

USERNAME = "dummy_2070"
PASSWORD = "sun@bun"

def init_driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

def login(driver):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)

    driver.find_element(By.NAME, "username").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD + Keys.RETURN)
    time.sleep(7)

def handle_post_login_popups(driver):
    wait = WebDriverWait(driver, 10)
    try:
        # Dismiss "Save Your Login Info?"
        not_now_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Not Now')]")))
        not_now_btn.click()
        time.sleep(2)
    except:
        pass

    try:
        # Dismiss "Turn on Notifications"
        turn_off_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Not Now')]")))
        turn_off_btn.click()
        time.sleep(2)
    except:
        pass

def search_user(driver, username):
    wait = WebDriverWait(driver, 15)

    # Sidebar search input
    search_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@aria-label='Search input']")
    ))
    search_input.clear()
    search_input.send_keys(username)
    time.sleep(2)

    # Click the first matching account
    profile_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//a[contains(@href, '/{username}/')]")
    ))
    profile_link.click()
    time.sleep(5)

def follow_if_not_following(driver):
    try:
        follow_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Follow' or contains(text(),'Follow')]")
            )
        )
        follow_btn.click()
        time.sleep(2)
    except:
        print("Already following or Follow button not found.")

def extract_info(driver):
    wait = WebDriverWait(driver, 10)
    username = "cbitosc"

    # Force a scroll to trigger lazy-load
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(5)

    try:
        name = driver.find_element(By.XPATH, "//h1").text.strip()
    except:
        name = ""

    try:
        stats = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//ul/li//span[contains(@class,'_ac2a') or contains(@class,'_ac2b')]")
        ))
        posts, followers, following = [s.text.strip() for s in stats[:3]]
    except:
        posts = followers = following = "N/A"

    try:
        bio_elem = driver.find_element(By.XPATH, "//div[contains(@class, '_aa_c')]/div")
        bio = bio_elem.text.strip() if bio_elem else "N/A"
    except:
        bio = "N/A"

    with open("cbitosc_info.txt", "w", encoding="utf-8") as f:
        f.write(f"Username: {username}\n")
        f.write(f"Name: {name}\n")
        f.write(f"Posts: {posts}\n")
        f.write(f"Followers: {followers}\n")
        f.write(f"Following: {following}\n")
        f.write(f"Bio:\n{bio}")

    print("Profile data saved to cbitosc_info.txt")


if __name__ == "__main__":
    driver = init_driver()
    try:
        login(driver)
        handle_post_login_popups(driver)  
        search_user(driver, "cbitosc")
        follow_if_not_following(driver)
        extract_info(driver)
    finally:
        driver.quit()
