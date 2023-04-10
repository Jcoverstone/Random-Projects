import requests
from bs4 import BeautifulSoup
import re

class WebVulnerabilityScanner:
    
    def __init__(self, target_url, depth=1, max_urls=10):
        self.target_url = target_url
        self.session = requests.Session()
        self.urls_to_scan = [target_url]
        self.depth = depth
        self.max_urls = max_urls
        self.scanned_urls = []
        self.vulnerabilities = []

    def scan_url(self, url):
        soup = self.get_soup(url)
        forms = soup.find_all("form")
        for form in forms:
            vulnerabilities = self.scan_form(form, url)
            if vulnerabilities:
                self.vulnerabilities.extend(vulnerabilities)

    def scan_form(self, form, url):
        action = form.get("action")
        method = form.get("method")
        inputs = form.find_all("input")
        payload = {}
        for input in inputs:
            name = input.get("name")
            value = input.get("value")
            if name and value:
                payload[name] = value
        vulnerabilities = []
        if action and method in ["post", "POST"]:
            response = self.session.post(action, data=payload)
            vulnerabilities = self.check_response(response, payload, url)
        return vulnerabilities

    def check_response(self, response, payload, url):
        vulnerabilities = []
        if "password" in str(response.content):
            vulnerabilities.append("Password field found in response: " + url)
        if "username" in str(response.content):
            vulnerabilities.append("Username field found in response: " + url)
        if "login" in str(response.content):
            vulnerabilities.append("Login page found: " + url)
        return vulnerabilities

    def get_links(self, url):
        soup = self.get_soup(url)
        links = []
        for link in soup.find_all("a"):
            href = link.get("href")
            if href:
                if self.target_url in href and href not in self.scanned_urls and href not in self.urls_to_scan:
                    links.append(href)
        return links

    def get_soup(self, url):
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            return soup
        except requests.exceptions.RequestException:
            return None

    def run_scan(self):
        for i in range(self.depth):
            for url in self.urls_to_scan:
                if url not in self.scanned_urls:
                    self.scan_url(url)
                    self.scanned_urls.append(url)
                    links = self.get_links(url)
                    self.urls_to_scan.extend(links[:self.max_urls])
                if len(self.scanned_urls) >= self.max_urls:
                    return

    def print_vulnerabilities(self):
        if not self.vulnerabilities:
            print("No vulnerabilities found.")
        else:
            print("Vulnerabilities found:")
            for vulnerability in self.vulnerabilities:
                print("- " + vulnerability)

    def save_vulnerabilities(self, filename):
        if not self.vulnerabilities:
            print("No vulnerabilities found.")
        else:
            with open(filename, "w") as f:
                f.write("Vulnerabilities found:\n")
                for vulnerability in self.vulnerabilities:
                    f.write("- " + vulnerability + "\n")

    def clear_vulnerabilities(self):
        self.vulnerabilities = []
