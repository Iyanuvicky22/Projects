from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time
import random
from utils.logger_config import logger
import requests
import bs4
import re
import csv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.utils import dump_raw_data_to_s3

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f'data/{timestamp}_ai_tools_scraped.csv'
os.makedirs(os.path.dirname(filename), exist_ok=True)


def extract_tool_data(element):
    tool_data = {}

    title_selectors = [
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        '[class*="sv-tile__title sv-text-reset sv-is-link"]'  # Standard headings
        ".title",
        ".name",
        ".tool-name",
        ".product-name",  # Common title classes
        '[class*="title"]',
        '[class*="name"]',  # Partial class matches
        "a[href]",  # Links often contain tool names
        "strong",
        "b",  # Bold text
        ".sv-tile-title",
        ".sv-title",  # SV-specific classes
    ]

    for selector in title_selectors:
        title_elem = element.select_one(selector)
        if title_elem and title_elem.get_text(strip=True):
            title_text = title_elem.get_text(strip=True)
            # Skip very short or very long titles
            if 3 <= len(title_text) <= 100:
                tool_data["name"] = title_text
                break

    desc_selectors = [
        ".description",
        ".desc",
        ".summary",
        ".overview",
        '[class*="desc"]',
        '[class*="summary"]',
        "p",  # Paragraphs
        "sv-tile__description sv-text-reset",
        ".sv-tile-description",
        ".sv-description",  # SV-specific
    ]

    for selector in desc_selectors:
        desc_elem = element.select_one(selector)
        if desc_elem and desc_elem.get_text(strip=True):
            desc_text = desc_elem.get_text(strip=True)
            # Look for meaningful descriptions (not too short, not the same as title)
            if len(desc_text) > 20 and desc_text != tool_data.get("name", ""):
                tool_data["description"] = desc_text
                break

    if not tool_data.get("description"):
        all_text_elements = element.find_all(string=True)
        text_contents = [text.strip() for text in all_text_elements if text.strip()]
        if text_contents:
            # Find the longest text that's not the title
            longest_text = max(text_contents, key=len, default="")
            if len(longest_text) > 20 and longest_text != tool_data.get("name", ""):
                tool_data["description"] = longest_text

    link_elements = element.select("a[href]")
    for link_elem in link_elements:
        href = link_elem.get("href", "")
        if href and not href.startswith("#"):
            if href.startswith("http"):
                tool_data["url"] = href
                break
            elif href.startswith("/") and "aitoolsdirectory.com" not in href:
                # Skip internal directory links, look for external ones
                continue
            elif href.startswith("/"):
                tool_data["url"] = f"https://aitoolsdirectory.com{href}"

    tool_data["source"] = "https://aitoolsdirectory.com"

    tag_selectors = [
        ".tag",
        ".category",
        ".badge",
        ".label",
        ".chip",
        '[class*="tag"]',
        '[class*="category"]',
        '[class*="badge"]',
        ".sv-tag",
        ".sv-category",  # SV-specific
    ]

    tags = []
    for selector in tag_selectors:
        tag_elements = element.select(selector)
        for tag_elem in tag_elements:
            tag_text = tag_elem.get_text(strip=True)
            if tag_text and 2 <= len(tag_text) <= 30:  # Reasonable tag length
                tags.append(tag_text)

    if tags:
        tool_data['category'] = tags[0]

    return tool_data


def save_tools(tools):
    if not tools:
        logger.warning("No tools to save.")
        return
    file_exists = os.path.isfile(filename)
    fieldnames = tools[0].keys()

    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerows(tools)
        print(f"Appended {len(tools)} tools to {filename}")
    except Exception as e:
        print(f"Failed to append tools to CSV: {e}")


class AIToolsScraper:
    def __init__(self, headless=True, wait_time=10):
        self.wait_time = wait_time
        self.setup_driver(headless)
        self.tools = []

    def setup_driver(self, headless=True):
        chrome_options = Options()

        if headless:
            chrome_options.add_argument("--headless")

        # Anti-detection measures
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        # Realistic browser settings
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")

        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            self.wait = WebDriverWait(self.driver, self.wait_time)
            logger.info("WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise

    def wait_for_content_load(self, max_wait=30):
        logger.info("Waiting for content to load...")
        if self.wait_for_main_list():
            return True

    def wait_for_elements(self, selectors, timeout=15):
        for selector in selectors:
            try:
                element = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if element:
                    logger.info(f"Found elements with selector: {selector}")
                    return True
            except TimeoutException:
                continue
        return False

    def wait_for_main_list(self, timeout=20):
        main_list_selector = ".sv-tiles-list.sv-tiles-list--flex.sv-tiles-list--tile-view.sv-tiles-list--small-size"
        try:
            logger.info("Waiting for main tools list to load...")
            element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, main_list_selector))
            )

            tools_selector = f"{main_list_selector} > *"
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, tools_selector))
            )

            logger.info("Main tools list loaded successfully")
            return True
        except TimeoutException:
            logger.warning("Main tools list not found within timeout")
            return False

    def wait_for_network_idle(self, timeout=20):
        try:
            self.driver.execute_async_script(
                """
                var callback = arguments[arguments.length - 1];
                var timeout = setTimeout(function() {
                    callback(true);
                }, arguments[0] * 1000);

                // Override fetch and XMLHttpRequest to track requests
                var pendingRequests = 0;
                var originalFetch = window.fetch;
                var originalXHR = window.XMLHttpRequest.prototype.open;

                window.fetch = function() {
                    pendingRequests++;
                    return originalFetch.apply(this, arguments).finally(() => {
                        pendingRequests--;
                        if (pendingRequests === 0) {
                            clearTimeout(timeout);
                            callback(true);
                        }
                    });
                };
            """,
                timeout,
            )
            return True
        except:
            return False

    def wait_for_page_ready(self):
        try:
            # Wait for document ready
            self.wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                               == "complete"
            )

            # Wait for common loading indicators to disappear
            loading_selectors = [
                ".loading",
                ".spinner",
                ".loader",
                '[class*="loading"]',
                '[class*="spinner"]',
                '[class*="loader"]',
            ]

            for selector in loading_selectors:
                try:
                    self.wait.until(
                        EC.invisibility_of_element_located((By.CSS_SELECTOR, selector))
                    )
                except TimeoutException:
                    pass  # Loading indicator might not exist

            return True
        except:
            return False

    def scroll_to_load_content(self):
        logger.info("Scrolling to trigger lazy loading...")

        # Get initial height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        scroll_attempts = 0
        max_attempts = 5

        while scroll_attempts < max_attempts:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(2)

            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height
            scroll_attempts += 1
            logger.info(f"Scroll attempt {scroll_attempts}, new height: {new_height}")

        # Scroll back to top
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

    def extract_tools_from_page(self):
        logger.info("Extracting tools from page...")

        # Get page source after JavaScript execution
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # First, try to find the main tools list container
        main_list_selector = "div.sv-tiles-list.sv-tiles-list--flex.sv-tiles-list--tile-view.sv-tiles-list--small-size"
        main_list = soup.select_one(main_list_selector)

        tools_found = []

        if main_list:
            logger.info("Found main tools list container")

            tool_elements = main_list.find_all(recursive=False)
            logger.info(
                f"Found {len(tool_elements)} direct child elements in main list"
            )

            if not tool_elements:
                tool_elements = main_list.find_all(["div", "article", "section"])
                logger.info(
                    f"Found {len(tool_elements)} descendant elements in main list"
                )

            # Extract data from each tool element
            for element in tool_elements:
                tool_data = extract_tool_data(element)
                if tool_data and tool_data.get("name"):
                    tools_found.append(tool_data)

        logger.info(f"Extracted {len(tools_found)} tools from current page")
        return tools_found

    def save_page_html(self, filename="debug_page.html"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        logger.info(f"Page HTML saved to {filename}")

    def scrape_page(self, url, page_num=1):
        logger.info(f"Scraping page {page_num}: {url}")

        try:
            self.driver.get(url)
            self.wait_for_content_load()
            self.scroll_to_load_content()

            tools = self.extract_tools_from_page()

            return tools

        except Exception as e:
            logger.error(f"Error scraping page {page_num}: {e}")
            return []

    def scrape_multiple_pages(self, base_url, max_pages=5):
        all_tools = []

        for page in range(1, max_pages + 1):
            url = f"{base_url}?page={page}"

            page_tools = self.scrape_page(url, page)
            all_tools.extend(page_tools)

            if page < max_pages:
                delay = random.uniform(2, 5)
                logger.info(f"Waiting {delay:.1f} seconds before next page...")
                time.sleep(delay)

        logger.info(f"Total unique tools scraped: {len(all_tools)}")

        return all_tools

    def close(self):
        if hasattr(self, "driver"):
            self.driver.quit()
            logger.info("WebDriver closed")

    def scrape_toolify_categories(self):
        logger.info("Starting scrape_toolify_categories function")
        data = []

        try:
            logger.info("Fetching page from https://www.toolify.ai/category")
            res = requests.get("https://www.toolify.ai/category", timeout=50)
            res.raise_for_status()
            logger.info(f"Successfully fetched page, status code: {res.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch page: {e}")
            return data

        try:
            logger.info("Starting HTML parsing")
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            table = soup.find_all('div', id=re.compile(r'^group-'))
            logger.info(f"Found {len(table)} category groups")

            if not table:
                logger.warning("No category groups found with id starting with 'group-'")

            for i, row in enumerate(table):
                logger.debug(f"Processing category group {i + 1}/{len(table)}")
                try:
                    title = row.find('h3').get_text(strip=True)
                    logger.debug(f"Found category: {title}")
                    sub_categories = []

                    sub_links = row.find_all('a', class_='go-category-link')
                    logger.debug(f"Found {len(sub_links)} subcategories for '{title}'")

                    for j, sub_row in enumerate(sub_links):
                        href = sub_row.get('href', '')
                        full_link = f"https://www.toolify.ai{href}" if href.startswith('/') else href

                        name_span = sub_row.find('span',
                                                 class_='text-base text-gray-1000 flex-1 w-0 truncate font-medium')
                        if name_span:
                            name = name_span.get_text(strip=True)
                            sub_categories.append({
                                'name': name,
                                'link': full_link,
                            })
                            logger.debug(f"Added subcategory: {name}")
                        else:
                            logger.info(f"Skipping subcategory {j + 1} in '{title}' - no expected span found")

                    data.append({
                        'category': title,
                        'sub_categories': sub_categories
                    })
                    logger.info(f"Successfully processed category '{title}' with {len(sub_categories)} subcategories")
                except AttributeError as e:
                    logger.warning(f"Could not extract category block {i + 1} properly: {e}")
        except Exception as e:
            logger.error(f"Unexpected parsing error: {e}")

        logger.info(f"scrape_toolify_categories completed successfully. Extracted {len(data)} categories")
        return data

    def scrape_toolify_subcategory(self, subcategory_url, category_name="", subcategory_name=""):
        logger.info(f"Starting scrape_toolify_subcategory for URL: {subcategory_url}, category: {category_name}, "
                    f"subcategory: {subcategory_name}")
        sub_data = []

        try:
            logger.info(f"Fetching subcategory page: {subcategory_url}")
            res = requests.get(subcategory_url, timeout=50)
            res.raise_for_status()
            logger.info(f"Successfully fetched subcategory page, status code: {res.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch subcategory page: {e}")
            return sub_data

        try:
            logger.info("Starting HTML parsing for subcategory")
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            table = soup.find_all('div', class_='mb-12')
            logger.info(f"Found {len(table)} tool items in subcategory")

            for i, row in enumerate(table):
                logger.debug(f"Processing tool item {i + 1}/{len(table)}")
                try:
                    row_class = row.find('div', class_='tool-card bg-white p-6 flex gap-4 items-center')
                    agent = row_class.find('div',
                                           class_='card-text-content flex flex-col justify-between flex-1 h-full w-0')

                    name = agent.find('a').find('h2').get_text(strip=True)
                    description = agent.find('p').get_text(strip=True)
                    full_url = ''
                    visit_btn_parent = row.find('div', class_='visit-btn')
                    if visit_btn_parent:
                        visit_link_tag = visit_btn_parent.find_parent('a')  # Get the <a> that wraps the button
                        if visit_link_tag and visit_link_tag.has_attr('href'):
                            visit_url = visit_link_tag['href']
                            full_url = visit_url

                    tool_data = {
                        "name": name,
                        "description": description,
                        "url": full_url,
                        "source": "https://www.toolify.ai",
                        "category": category_name
                    }

                    sub_data.append(tool_data)
                    logger.debug(f"Successfully extracted tool: {name}")


                except AttributeError as e:
                    logger.warning(f"Could not parse tool item {i + 1}: {e}")

        except Exception as e:
            logger.error(f"Unexpected parsing error in subcategory scraping: {e}")

        logger.info(
            f"scrape_toolify_subcategory completed. Extracted {len(sub_data)} tools from category '{category_name}'")
        return sub_data

    def scrape_all_toolify_data_concurrent(self, max_workers=10):
        all_tools = []
        categories = self.scrape_toolify_categories()
        subcat_jobs = []

        for category in categories:
            category_name = category['category']
            for subcat in category.get('sub_categories', []):
                subcat_name = subcat['name']
                subcat_url = subcat['link']
                subcat_jobs.append((category_name, subcat_url, subcat_name))

        print(f"[INFO] Queued {len(subcat_jobs)} subcategories for scraping")

        # Threaded scraping
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_subcat = {
                executor.submit(self.scrape_toolify_subcategory, url, category_name, subcategory): subcategory
                for category_name, url, subcategory in subcat_jobs
            }

            for future in as_completed(future_to_subcat):
                subcat_name = future_to_subcat[future]
                try:
                    result = future.result()
                    save_tools(result)
                    all_tools.extend(result)
                    logger.debug(f"Saved tool data for: {subcat_name}")
                    print(f"[DONE] Scraped {len(result)} tools from: {subcat_name}")
                except Exception as e:
                    print(f"[ERROR] Failed scraping {subcat_name}: {e}")
        print(f"[DONE] Scraped {len(all_tools)} tools in total")
        return all_tools


def main(all_page: int):
    scraper = None

    try:
        print("AI Tools Directory Scraper")
        print("=" * 40)

        scraper = AIToolsScraper(wait_time=15)
        base_url = "https://aitoolsdirectory.com/"

        max_pages = all_page
        max_pages = min(max_pages, 10)

        print(f"\nStarting to scrape {max_pages} pages...")
        tools = scraper.scrape_multiple_pages(base_url, max_pages)

        if tools:
            print(f"\n{'=' * 60}")
            print(f"SCRAPING COMPLETED - Found {len(tools)} unique AI tools")
            print(f"{'=' * 60}")

            save_tools(tools)

        else:
            print("No tools were scraped. The website structure might have changed.")
        # scrape toolify website
        scraper.scrape_all_toolify_data_concurrent()
        dump_raw_data_to_s3(filename)

    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
    except Exception as e:
        logger.error(f"Scraping failed: {e}")

    finally:
        if scraper:
            scraper.close()


if __name__ == "__main__":
    main(4)
    # dump_raw_data_to_s3('data/20250601_231255_ai_tools_scraped.csv')
    #
