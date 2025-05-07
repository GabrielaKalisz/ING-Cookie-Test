from playwright.sync_api import sync_playwright


def test_accept_analytics_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.ing.pl")
        page.get_by_role("button", name="Dostosuj").click()
        #page.get_by_role("switch", name="Cookies analityczne").locator("span").first.click()
        page.get_by_role("switch", name="Cookies marketingowe").locator("span").nth(1).click()
        page.get_by_role("button", name="Zaakceptuj zaznaczone").click()

        cookies = page.context.cookies()
        policy_cookie = next((cookie for cookie in cookies if cookie["name"] == "cookiePolicyGDPR"), None)


        assert policy_cookie is not None, "Brak cookiePolicyGDPR – nie zapisano ustawień cookies"
        print("Test nieudany")
        assert policy_cookie["value"] == "3", "Oczekiwano wartości '3' dla analitycznych, otrzymano: " + policy_cookie[
            "value"]
        print("Test przeszedł pomyślnie – znaleziono poprawne cookie 'cookiePolicyGDPR'")

        browser.close()
