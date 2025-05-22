import allure
import pytest
import requests
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from selene import browser, have

LOGIN = "ivan@ya.ru"
PASSWORD = "123456"
WEB_URL = "https://demowebshop.tricentis.com/"
API_URL = "https://demowebshop.tricentis.com/"


@pytest.fixture(scope='function', autouse=True)
def clean_cart():
    yield
    browser.element('[name="removefromcart"]').click()
    browser.element('[name="updatecart"]').click()


def test_add_book_in_cart():
    with step("Login with API"):
        result = requests.post(
            url=API_URL + "/login",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )
        allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")
    with step("Get cookie from API"):
        cookie = result.cookies.get("NOPCOMMERCE.AUTH")

    with step("Set cookie from API"):
        browser.open(WEB_URL)
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open(WEB_URL)

    with step("add book in cart with API"):
        requests.post("https://demowebshop.tricentis.com/addproducttocart/catalog/13/1/1",
                      cookies={'NOPCOMMERCE.AUTH': cookie})

    with step("Verify add in cart"):
        browser.element("#topcartlink").click()
        browser.element(".product-name").should(have.exact_text('Computing and Internet'))


def test_add_jewelry_in_cart():
    with step("Login with API"):
        result = requests.post(
            url=API_URL + "/login",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )
        allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")
    with step("Get cookie from API"):
        cookie = result.cookies.get("NOPCOMMERCE.AUTH")

    with step("Set cookie from API"):
        browser.open(WEB_URL)
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open(WEB_URL)

    with step("clean cart"):
        requests.post("https://demowebshop.tricentis.com/cart", cookies={'NOPCOMMERCE.AUTH': cookie})

    with step("add jewelery in cart with API"):
        requests.post("https://demowebshop.tricentis.com/addproducttocart/catalog/14/1/1",
                      cookies={'NOPCOMMERCE.AUTH': cookie})

    with step("Verify add in cart"):
        browser.element("#topcartlink").click()
        browser.element(".product-name").should(have.exact_text('Black & White Diamond Heart'))
