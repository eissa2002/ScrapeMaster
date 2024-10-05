from youtube_scraper import YouTubeChannelScraper, YouTubeVideoScraper
from image_scraper import ImageScraper
from link_scraper import WebsiteLinkScraper

# Main function to execute scraping tasks
if __name__ == "__main__":
    driver_path = r"C:\Users\eissa\Downloads\chromedriver-win64\chromedriver.exe"

    # Step 1: Scrape YouTube channels based on search query
    channel_scraper = YouTubeChannelScraper(driver_path)
    content_search = "Engineering"
    desired_channel_count = 10  # Scrape 10 channels for this example
    channel_links = channel_scraper.scrape_channel_links(content_search, desired_channel_count)

    # Step 2: Scrape videos from the scraped channels
    video_scraper = YouTubeVideoScraper(driver_path)
    all_video_links = video_scraper.scrape_videos_from_channels(channel_links, max_videos_per_channel=50)

    # Display video scraping results
    for channel, videos in all_video_links.items():
        print(f"\nVideos from {channel}:")
        for video in videos:
            print(video)

    # Step 3: Scrape related websites and images
    website_scraper = WebsiteLinkScraper(driver_path)
    websites = website_scraper.search_for_websites("Engineering", num_results=30)

    # Step 4: Scrape images from these websites
    image_scraper = ImageScraper(driver_path)
    image_scraper.scrape_images("Engineering", websites, save_folder="engineering_images")

    print("Scraping task completed.")
