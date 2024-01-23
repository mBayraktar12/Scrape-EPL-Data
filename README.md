# Premier League Data Scraping

This Python script scrapes data from the Premier League using BeautifulSoup and Pandas. It collects match and shooting statistics for each Premier League team over multiple seasons and stores the data in a CSV file.

## Prerequisites

Before running the script, make sure you have the following Python libraries installed:

- requests
- BeautifulSoup (bs4)
- pandas

You can install them using pip:

`pip install requests beautifulsoup4 pandas`


## Usage

1. Clone or download this repository to your local machine.

2. Open a terminal or command prompt and navigate to the project directory.

3. Run the script by executing the following command:

`python scrape.py`

4. The script will start scraping data from the website, and the collected data will be saved to a file named `matches.csv` in the same directory.

## Configuration

You can adjust the scraping behavior by modifying the constants in the script:

- `DATA_DELAY`: Adjust the delay (in seconds) between web requests to avoid overloading the website's server.

## Troubleshooting

If you encounter any issues or errors while running the script, feel free to open an issue in this repository, and we'll do our best to help you.
