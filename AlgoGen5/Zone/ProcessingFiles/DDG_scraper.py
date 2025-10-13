from playwright.sync_api import sync_playwright

def duckduckgo_search(query):
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # можешь поставить False — чтобы видеть
        page = browser.new_page()
        page.goto("https://duckduckgo.com/")
        page.fill("input[name='q']", query)
        page.keyboard.press("Enter")
        page.wait_for_selector(".result__url", timeout=10000)

        links = page.query_selector_all(".result__url")
        for link in links:
            href = link.get_attribute("href")
            if href:
                results.append(href)

        browser.close()
    return results