
# 📺 YouTube & 🌐 Image Scraper

### Description

This is an automated scraper tool for retrieving YouTube channel links, scraping video links from those channels, and finding images and links related to your query from websites. Built with Python using Selenium and BeautifulSoup, this tool also features a modern, eye-catching GUI to make it user-friendly and efficient for your team.

---

### Key Features

- **YouTube Channel Scraper**: 
    - Search and scrape YouTube channels based on your query.
    - Retrieve and display links for the specified number of channels.
    
- **YouTube Video Scraper**:
    - Scrape video links from each YouTube channel.
    - Customize the number of videos you want to scrape from each channel.

- **Image and Link Scraper**:
    - Search Google for websites related to your query.
    - Scrape and download images from the retrieved websites.
    - Download and log the image URLs.

- **GUI Interface**:
    - A modern GUI built with `Tkinter`.
    - Input your YouTube search query, number of channels, and number of videos per channel.
    - Browse and choose a folder to save the scraped images.
    - Visual feedback with a progress bar and status logs during scraping.

---

### Tech Stack

- **Language**: Python
- **Libraries**:
    - `Selenium`
    - `BeautifulSoup` (`bs4`)
    - `Tkinter` (GUI)
    - `requests` (Image downloads)

---

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Install the required Python packages**:

   You can use `pip` to install the required dependencies listed in the `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Download ChromeDriver**:

   Ensure that you have [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) installed and that it matches your Chrome browser version. Place it in a folder and update the `driver_path` in the code.

---

### Usage

1. **Run the GUI application**:

   Run the Python GUI application:

   ```bash
   python gui.py
   ```

2. **Use the GUI**:

   - Input your YouTube search query (e.g., "Engineering").
   - Enter the number of channels to scrape and the number of videos per channel.
   - Select a folder to save the scraped images.
   - Click `Start Scraping` and watch the progress!

---


### Requirements

- Python 3.x
- Chrome browser
- ChromeDriver (matching your Chrome version)

---

### Contributing

1. **Fork** the repository.
2. **Create** a feature branch (`git checkout -b feature-branch`).
3. **Commit** your changes (`git commit -m 'Add feature'`).
4. **Push** to the branch (`git push origin feature-branch`).
5. **Create** a new Pull Request.

---

### License

This project is licensed under the MIT License.

---

### Screenshots
<img src="https://github.com/user-attachments/assets/7c669b0e-b50b-424d-9cec-94dbed24c0f2" alt="image" width="600"/>
