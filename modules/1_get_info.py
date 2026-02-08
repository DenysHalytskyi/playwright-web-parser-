"""The script collects product data and stores it in a Postgres database."""

from load_django import *
from parser_app.models import *
import asyncio
from playwright.async_api import async_playwright
from playwright.async_api import TimeoutError
from pprint import pprint
from asgiref.sync import sync_to_async


def save_data(data):
    try:
        obj, created = Product.objects.get_or_create(**data)
        status = "created" if created else "already exists"
        print(f"{obj.full_name} ({obj.product_code}) ({status})")
    except Product.MultipleObjectsReturned:
        print("Multiple products found")


async def main():

    product_info = {}
    images_list = []
    specs = {}


    try:
        async with (async_playwright() as p):
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            await page.goto("https://brain.com.ua/")

            search_input = page.locator('input.quick-search-input:visible').first

            await search_input.wait_for(state="visible")

            await search_input.fill("Apple iPhone 15 128GB Black")

            await page.keyboard.press("Enter")

            iphone_first = page.locator('div.product-wrapper:visible').first
            await iphone_first.locator('div.br-pp-ipd-hidden > a').click()

            try:    #full name
                full_name = await page.locator('span.product-clean-name').first.inner_text()
                product_info["full_name"] = full_name.strip()

            except AttributeError as e:
                product_info["full_name"] = None

            try:    #price
                main_price = await page.locator('div.br-pr-op span').first.inner_text()
                product_info["main_price"] = int(main_price.replace(' ', ''))

            except TimeoutError as e:
                product_info["main_price"] = None

            try:    #red price
                red_price = await page.locator('div.br-pr-np span').first.inner_text()
                product_info["red_price"] = int(red_price.replace(' ', ''))

            except TimeoutError as e:
                product_info["red_price"] = None

            try:    #product code
                product_code = await page.locator('div#product_code span.br-pr-code-val:visible').first.inner_text()
                product_info["product_code"] = product_code.strip()

            except TimeoutError as e:
                product_info["product_code"] = None

            try:    #review
                review = await page.locator('div#br-pr-1 a.brackets-reviews:visible').first.inner_text()
                review_count = ''.join(filter(str.isdigit, review))
                product_info["review_count"] = review_count.strip()

            except TimeoutError as e:
                product_info["review_count"] = None

            try:    #images
                images = await page.locator('div.br-image-links img').all()
                for image in images:
                    src = await image.get_attribute('src')
                    images_list.append(src)
                product_info["images"] = images_list

            except Exception as e:
                product_info["images"] = None

            try:    #characteristics
                await page.locator("#br-pr-1 a.scroll-to-element-after:visible").first.click()
                await page.wait_for_timeout(2000)

                specs_blocks = await page.locator('#br-pr-7 div.br-pr-chr-item').all()
                for block in specs_blocks:
                    rows = await block.locator(':scope > div > div').all()
                    for row in rows:
                        spans = await row.locator('span').all()
                        if len(spans) == 2:
                            key = (await spans[0].inner_text()).strip()
                            value = (await spans[1].inner_text()).replace('\xa0', ' ').strip()
                            specs[key] = value

                product_info["characteristics"] = specs

            except TimeoutError as e:
                product_info["characteristics"] = None

            try:
                product_info["color"] = specs["Колір"]
            except AttributeError as e:
                product_info["color"] = None
            try:
                product_info["memory"] = specs["Вбудована пам'ять"]
            except AttributeError as e:
                product_info["memory"] = None
            try:
                product_info["producer"] = specs["Виробник"]
            except AttributeError as e:
                product_info["producer"] = None
            try:
                product_info["diagonal"] = specs["Діагональ екрану"]
            except AttributeError as e:
                product_info["diagonal"] = None
            try:
                product_info["resolution"] = specs["Роздільна здатність екрану"]
            except AttributeError as e:
                product_info["resolution"] = None


            await browser.close()

    except Exception as e:
        print(f"Error: {e}")
    "qwertyu"

    pprint(product_info, sort_dicts=False)


"""
    data_to_save = {
        "full_name": product_info["full_name"],
        "product_code": product_info["product_code"],
        "main_price": product_info["main_price"],
        "red_price": product_info["red_price"],
        "review_count": product_info["review_count"],
        "color": product_info["color"],
        "memory": product_info["memory"],
        "producer": product_info["producer"],
        "screen_diagonal": product_info["diagonal"],
        "display_resolution": product_info["resolution"],
        "image": product_info["images"],
        "characteristics": product_info["characteristics"],
    }

    await sync_to_async(save_data)(data_to_save)
"""



if __name__ == "__main__":
    asyncio.run(main())
