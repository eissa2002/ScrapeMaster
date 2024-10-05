import time

def scroll_down(driver, scroll_pause_time=2, max_scroll_attempts=50):
    """Scrolls down the page to load more content."""
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    scroll_attempts = 0

    while scroll_attempts < max_scroll_attempts:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(scroll_pause_time)
        
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            print(f"Scroll completed after {scroll_attempts} attempts, no more content to load.")
            break
        
        last_height = new_height
        scroll_attempts += 1
        print(f"Scrolled {scroll_attempts} times.")
