import requests
import random
import colorama
import threading


class Listing:
    def __init__(self, link):
        self.link = link
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        }
        self.success_count = 0
        self.lock = threading.Lock()

    def add_ebay_views(self, num=1):
        proxies = self.load_proxies()
        threads = []

        for _ in range(num):
            proxy = random.choice(proxies).strip()
            thread = threading.Thread(target=self._ebay_view, args=(proxy,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        success_rate = (self.success_count / num) * 100 if num else 0
        print(f"{colorama.Fore.BLUE}{self.success_count}/{num}: {success_rate:.2f}%{colorama.Style.RESET_ALL}\n\n")
        return self.success_count

    def _ebay_view(self, proxy):
        """Add view to EbayListing"""
        try:
            response = requests.get(self.link, headers=self.headers, proxies={"http": proxy}, timeout=10)
            if response.status_code == 200:
                with self.lock:
                    print(f"Product page opened successfully on proxy: {colorama.Fore.LIGHTGREEN_EX}{proxy}{colorama.Style.RESET_ALL}")
                    self.success_count += 1
            else:
                print(f"{colorama.Fore.YELLOW}{response.status_code} response, failed opening page on proxy: {colorama.Fore.LIGHTRED_EX}{proxy}{colorama.Style.RESET_ALL}")
        except requests.exceptions.RequestException as e:
            print(f"Error with requests on proxy: {colorama.Fore.LIGHTRED_EX}{proxy}{colorama.Style.RESET_ALL} {colorama.Fore.RED}{e}{colorama.Style.RESET_ALL}")

    def load_proxies(self):
        """Load proxies from file."""
        with open("proxies.txt", "r") as f:
            return f.readlines()


if __name__ == "__main__":
    link = input("Link Here: ")
    listing = Listing(link)
    count = int(input("View_Count: "))
    listing.add_ebay_views(count)  # Replace 10 with the number of views you want to add
