from logging import basicConfig, getLogger, INFO
from requests import Session, RequestException
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
from re import sub
import csv

basicConfig(level=INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = getLogger(__name__)


class BooksScraper:
    """
    Class to scrape book data from a website.
    This class handles fetching book details, parsing HTML content.
    """

    def __init__(self, base_url="https://books.toscrape.com/") -> None:
        """
        Initialize the scraper with the base URL.
        Args:
            base_url (str): Base URL of the website to scrape.
        """
        self.base_url = base_url
        self.session = Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

    def __fix_encoding(self, text: str) -> str:
        """
        Fix encoding issues in the text.
        Args:
            text (str): Text to fix encoding for.
        Returns:
            str: Text with fixed encoding.
        """
        return text.encode("latin1").decode("utf-8", errors="ignore")

    def __get_page_content(self, url: str) -> str:
        """
        Get the HTML content of a page.
        Args:
            url (str): URL of the page to fetch.
        Returns:
            str: HTML content of the page, or None if an error occurs.
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def __parse_price(self, price_text: str) -> float:
        """
        Convete price text to float.
        Args:
            price_text (str): Price text to parse.
        Returns:
            float: Parsed price as a float, or 0.0 if parsing fails.
        """
        if not price_text:
            return 0.0
        price_clean = sub(r"[^\d.]", "", price_text)
        try:
            return float(price_clean)
        except ValueError:
            return 0.0

    def __extract_book_details(self, book_url: str) -> dict:
        """
        Extract details from a book's detail page.
        Args:
            book_url (str): URL of the book's detail page.
        Returns:
            dict: Dictionary containing book details like description.
        """
        logger.info(f"Fetching book details from {book_url}...")
        content = self.__get_page_content(book_url)
        if not content:
            return None

        soup = BeautifulSoup(content, "html.parser")

        description = ""
        desc_div = soup.find("div", id="product_description")
        if desc_div:
            desc_p = desc_div.find_next_sibling("p")
            if desc_p:
                description = desc_p.get_text(strip=True)

        return description

    def __scrape_books_from_page(
        self, page_url: str, page_number: int = 1
    ) -> list[dict]:
        """
        Scrape books from a single page.
        Args:
            page_url (str): URL of the page to scrape.
            page_number (int): Current page number for logging.
        Returns:
            list: List of dictionaries containing book data.
        """
        content = self.__get_page_content(page_url)
        if not content:
            return []

        soup = BeautifulSoup(content, "html.parser")
        book_containers = soup.find_all("article", class_="product_pod")
        logger.info(f"Found {len(book_containers)} books on page {page_number}...")
        books = []
        for idx, book in enumerate(book_containers, 1):
            try:
                logger.info(
                    f"Processing book {idx} of {len(book_containers)} on page {page_number}..."
                )
                book_data = self.__extract_book_data(book, soup, page_number)
                books.append(book_data)
                logger.info(
                    f"Book {idx} extracted: {book_data['title']} - {book_data['price']} - {book_data['rating']} stars"
                )
                sleep(0.2)
            except Exception as e:
                logger.error(f"Error processing book {idx} on page {page_number}: {e}")
                continue

        next_page_url = self.__get_next_page_url(soup, page_url)
        if next_page_url:
            books += self.__scrape_books_from_page(next_page_url, page_number + 1)
        return books

    def __extract_book_data(
        self, book: BeautifulSoup, soup: BeautifulSoup, page_number: int
    ) -> dict:
        """
        Extracts data from a book element.
        Args:
            book (BeautifulSoup): BeautifulSoup object of the book element.
            soup (BeautifulSoup): BeautifulSoup object of the entire page.
            page_number (int): Current page number for logging.
        Returns:
            dict: Dictionary containing book data.
        """
        logger.info("Extracting book data...")

        title_link = book.find("h3").find("a")
        title = title_link.get("title") or title_link.get_text(strip=True)
        title = self.__fix_encoding(title)

        relative_url = title_link.get("href", "").lstrip("../")
        book_url = urljoin(self.base_url, f"catalogue/{relative_url}")

        logger.info(f"Book URL: {book_url}")

        price_text = book.find("p", class_="price_color").get_text(strip=True)
        price = self.__parse_price(price_text)

        ratting_element = book.find("p", class_="star-rating")
        rating = self.__parse_rating_from_classes(ratting_element)

        availability_element = book.find("p", class_="instock availability")
        availability = self.__parse_availability(availability_element)

        image_url = self.__extract_image_url(book)
        category = self.__extract_current_category(soup)

        logger.info(f"Looking for book details at {book_url}...")
        description = self.__extract_book_details(book_url)
        description = self.__fix_encoding(description)

        return {
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "category": category,
            "description": description,
            "image_url": image_url,
            "book_url": book_url,
            "page_number": page_number,
            "scraped_at": datetime.now().isoformat(),
        }

    def __parse_rating_from_classes(self, rating_element: BeautifulSoup) -> int:
        """
        Extract rating from the class attribute of the rating element.
        Args:
            rating_element (BeautifulSoup): BeautifulSoup object of the rating element.
        Returns:
            int: Rating as an integer (1-5), or 0 if not found.
        """

        if not rating_element:
            return 0

        rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

        for cls in rating_element.get("class", []):
            rating = rating_map.get(cls)
            if rating:
                return rating
        return 0

    def __parse_availability(self, element: BeautifulSoup) -> str:
        """
        Extracts the availability text from the element.
        Args:
            element (BeautifulSoup): BeautifulSoup object of the availability element.
        Returns:
            str: Cleaned availability text, or "Unknown" if not found.
        """
        if element:
            return " ".join(element.get_text(strip=True).split())
        return "Unknown"

    def __extract_image_url(self, book: BeautifulSoup) -> str:
        """
        Extracts the image URL from the book element.
        Args:
            book (BeautifulSoup): BeautifulSoup object of the book element.
        Returns:
            str: Full URL of the book's image, or an empty string if not found.
        """
        image_element = book.find("div", class_="image_container")
        if not image_element:
            return ""
        img_tag = image_element.find("img")
        if not img_tag:
            return ""
        relative_url = img_tag.get("src", "").lstrip("../")
        return urljoin(self.base_url, relative_url)

    def __extract_current_category(self, soup: BeautifulSoup) -> str:
        """
        Extracts the current category from the page.
        Args:
            soup (BeautifulSoup): BeautifulSoup object of the entire page.
        Returns:
            str: Name of the current category, or "Unknown" if not found.
        """
        h1_tag = soup.find("h1")
        if h1_tag:
            return h1_tag.get_text(strip=True)
        return "Unknown"

    def __get_all_category_urls(self) -> list[str]:
        """
        Extract all category URLs from the sidebar.
        Returns:
            list: List of category URLs.
        """
        logger.info("Extract all category URLs...")
        content = self.__get_page_content(self.base_url)
        if not content:
            return None

        soup = BeautifulSoup(content, "html.parser")
        category_urls = []

        sidebar = soup.find("div", class_="side_categories")
        if not sidebar:
            return None

        category_links = sidebar.find_all("a")
        for link in category_links:
            href = link.get("href")
            if "books_1" in href:
                continue
            if not href and href == "#":
                continue
            category_url = urljoin(self.base_url, href)
            category_urls.append(category_url)

        return category_urls

    def __get_next_page_url(self, soup: BeautifulSoup, current_url: str) -> str:
        """
        Extract the URL of the next page from the pagination.
        Args:
            soup (BeautifulSoup): Parsed HTML of the current page.
            current_url (str): URL of the current page.
        Returns:
            str: URL of the next page, or None if no next page exists.
        """
        next_li = soup.find("li", class_="next")
        if next_li and next_li.a:
            next_href = next_li.a.get("href")
            next_url = urljoin(current_url, next_href)
            return next_url
        return None

    def scrape_all_books(self) -> list[dict]:
        """
        Scrape all books from all categories.
        Returns:
            list: List of dictionaries containing book data.
        """
        logger.info("Iniciating scraping of all books...")
        all_books = []

        category_urls = self.__get_all_category_urls()

        if not category_urls:
            logger.warning("No category URLs found. Exiting scraping.")
            category_urls = [self.base_url]

        for category_url in category_urls:
            logger.info(f"Processing category: {category_url}")
            results = self.__scrape_books_from_page(category_url)
            logger.info(f"Found {len(results)} books in category {category_url}")
            all_books.extend(results)
        logger.info(f"Scraping completed. Total books found: {len(all_books)}")
        return all_books

    def save_to_csv(self, books, filename="books_data.csv"):
        """Salva os dados em arquivo CSV"""
        if not books:
            logger.warning("Nenhum livro para salvar.")
            return

        fieldnames = [
            "title",
            "price",
            "rating",
            "availability",
            "category",
            "description",
            "image_url",
            "book_url",
            "page_number",
            "scraped_at",
        ]

        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(books)

        logger.info(f"Dados salvos em {filename}")
