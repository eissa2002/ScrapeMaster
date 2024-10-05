import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from youtube_scraper import YouTubeChannelScraper, YouTubeVideoScraper
from image_scraper import ImageScraper
from link_scraper import WebsiteLinkScraper
import threading

class ScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📺 YouTube & 🌐 Image Scraper")
        self.root.geometry("700x500")
        self.root.configure(bg="#2C3E50")

        # Add title with custom font and color
        title_label = tk.Label(self.root, text="YouTube & Image Scraper", font=("Helvetica", 24, "bold"), bg="#2C3E50", fg="#ECF0F1")
        title_label.pack(pady=20)

        # Create GUI widgets
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root, bg="#2C3E50")
        frame.pack(pady=10)

        # YouTube Search Query
        tk.Label(frame, text="YouTube Search Query:", font=("Arial", 12), bg="#2C3E50", fg="#ECF0F1").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.query_entry = tk.Entry(frame, width=30, font=("Arial", 12))
        self.query_entry.grid(row=0, column=1, pady=10)

        # Number of Channels
        tk.Label(frame, text="Number of Channels:", font=("Arial", 12), bg="#2C3E50", fg="#ECF0F1").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.channel_count_entry = tk.Entry(frame, width=30, font=("Arial", 12))
        self.channel_count_entry.grid(row=1, column=1, pady=10)

        # Number of Videos per Channel
        tk.Label(frame, text="Videos per Channel:", font=("Arial", 12), bg="#2C3E50", fg="#ECF0F1").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.video_count_entry = tk.Entry(frame, width=30, font=("Arial", 12))
        self.video_count_entry.grid(row=2, column=1, pady=10)

        # Folder to Save Images
        tk.Label(frame, text="Image Save Folder:", font=("Arial", 12), bg="#2C3E50", fg="#ECF0F1").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.image_folder_entry = tk.Entry(frame, width=30, font=("Arial", 12))
        self.image_folder_entry.grid(row=3, column=1, pady=10)
        self.browse_button = ttk.Button(frame, text="Browse", command=self.browse_folder)
        self.browse_button.grid(row=3, column=2, padx=10)

        # Start Button with a custom color and style
        self.start_button = tk.Button(self.root, text="Start Scraping", font=("Arial", 14, "bold"), bg="#E74C3C", fg="white", command=self.start_scraping, relief="raised", bd=5)
        self.start_button.pack(pady=20)

        # Status/Progress Display
        self.status_text = tk.Text(self.root, height=8, width=70, bg="#34495E", fg="white", font=("Arial", 12))
        self.status_text.pack(pady=10)
        self.status_text.insert(tk.END, "Ready to start scraping...\n")

        # Progress bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=5)

    def browse_folder(self):
        """Select a folder to save images"""
        folder = filedialog.askdirectory()
        if folder:
            self.image_folder_entry.delete(0, tk.END)
            self.image_folder_entry.insert(0, folder)

    def log_message(self, message):
        """Log a message to the status box"""
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)

    def start_scraping(self):
        """Validate inputs and start scraping in a separate thread"""
        query = self.query_entry.get()
        try:
            num_channels = int(self.channel_count_entry.get())
            num_videos = int(self.video_count_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for channels and videos.")
            return
        
        save_folder = self.image_folder_entry.get()
        if not save_folder:
            messagebox.showerror("Folder Error", "Please select a folder to save images.")
            return
        
        # Disable Start button to prevent multiple clicks
        self.start_button.config(state=tk.DISABLED)

        # Reset progress bar and log
        self.progress["value"] = 0
        self.status_text.delete(1.0, tk.END)

        # Start the scraping in a separate thread to avoid freezing the GUI
        threading.Thread(target=self.scrape_content, args=(query, num_channels, num_videos, save_folder)).start()

    def scrape_content(self, query, num_channels, num_videos, save_folder):
        """Scraping YouTube channels, videos, and images based on the user input"""
        try:
            driver_path = r"C:\Users\eissa\Downloads\chromedriver-win64\chromedriver.exe"

            # Scrape YouTube channels
            channel_scraper = YouTubeChannelScraper(driver_path)
            self.log_message(f"Starting to scrape {num_channels} channels related to '{query}'...")
            channel_links = channel_scraper.scrape_channel_links(query, num_channels)

            # Update progress bar
            self.progress["maximum"] = num_channels + len(channel_links) + 1
            self.progress["value"] += 1

            # Scrape videos from each channel
            video_scraper = YouTubeVideoScraper(driver_path)
            self.log_message("Scraping videos from the scraped channels...")
            all_video_links = video_scraper.scrape_videos_from_channels(channel_links, max_videos_per_channel=num_videos)

            # Display video links
            for channel, videos in all_video_links.items():
                self.log_message(f"\nVideos from {channel}:")
                for video in videos:
                    self.log_message(video)
                self.progress["value"] += 1

            # Search for related websites and scrape images
            website_scraper = WebsiteLinkScraper(driver_path)
            self.log_message(f"\nSearching for websites related to '{query}'...")
            websites = website_scraper.search_for_websites(query, num_results=30)

            # Scrape images from websites
            image_scraper = ImageScraper(driver_path)
            self.log_message(f"Scraping images from related websites...")
            image_scraper.scrape_images(query, websites, save_folder)

            self.log_message("Scraping task completed.")
        except Exception as e:
            self.log_message(f"Error: {e}")
        finally:
            self.start_button.config(state=tk.NORMAL)
            self.progress["value"] = self.progress["maximum"]


if __name__ == "__main__":
    root = tk.Tk()
    app = ScraperGUI(root)
    root.mainloop()
