from playwright.sync_api import sync_playwright

def test_accept_analytics_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.ing.pl/")
        page.get_by_role("button", name="Dostosuj").click()
        page.get_by_role("switch", name="Cookies analityczne").locator("span").first.click()
        page.get_by_role("button", name="Zaakceptuj zaznaczone").click()

        cookies = page.context.cookies()
        policy_cookie = next((cookie for cookie in cookies if cookie["name"] == "cookiePolicyGDPR"), None)

        if policy_cookie is None:
            print("Test nieudany – nie znaleziono cookiePolicyGDPR")
            assert policy_cookie is not None, "Brak cookiePolicyGDPR – nie zapisano ustawień cookies"

        if policy_cookie["value"] != "3":
            print(f"Test nieudany – oczekiwano wartości '3'")
            assert policy_cookie["value"] == "3", f"Oczekiwano wartości '3' dla analitycznych, otrzymano: {policy_cookie['value']}"

        print("Test przeszedł pomyślnie – znaleziono poprawne cookie analityczne")

        browser.close()
