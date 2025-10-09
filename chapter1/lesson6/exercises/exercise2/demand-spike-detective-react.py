import ast
import datetime
import operator
import re
from typing import Optional, List, Dict, Any

import pandas as pd
from dotenv import load_dotenv

from app.util import OpenAIModels, openai_client, get_completion_v2

load_dotenv()

client = openai_client()
MODEL = OpenAIModels.GPT_41_MINI
SINGLE_TAB_LEVEL = 4


def get_sales_data(products: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    data = [
        {
            "date": datetime.date(2024, 1, 10),
            "product_id": "P001",
            "product_name": "Product 1",
            "quantity": 255,
            "revenue": 15547.35,
        },
        {
            "date": datetime.date(2024, 1, 10),
            "product_id": "P002",
            "product_name": "Product 2",
            "quantity": 65,
            "revenue": 2297.1,
        },
        {
            "date": datetime.date(2024, 1, 10),
            "product_id": "P003",
            "product_name": "Product 3",
            "quantity": 90,
            "revenue": 7301.7,
        },
        {
            "date": datetime.date(2024, 1, 10),
            "product_id": "P004",
            "product_name": "Product 4",
            "quantity": 171,
            "revenue": 8296.92,
        },
        {
            "date": datetime.date(2024, 1, 10),
            "product_id": "P005",
            "product_name": "Product 5",
            "quantity": 96,
            "revenue": 2587.2,
        },
        {
            "date": datetime.date(2024, 1, 11),
            "product_id": "P001",
            "product_name": "Product 1",
            "quantity": 235,
            "revenue": 14327.95,
        },
        {
            "date": datetime.date(2024, 1, 11),
            "product_id": "P002",
            "product_name": "Product 2",
            "quantity": 86,
            "revenue": 3039.24,
        },
        {
            "date": datetime.date(2024, 1, 11),
            "product_id": "P003",
            "product_name": "Product 3",
            "quantity": 79,
            "revenue": 6409.27,
        },
        {
            "date": datetime.date(2024, 1, 11),
            "product_id": "P004",
            "product_name": "Product 4",
            "quantity": 145,
            "revenue": 7035.4,
        },
        {
            "date": datetime.date(2024, 1, 11),
            "product_id": "P005",
            "product_name": "Product 5",
            "quantity": 114,
            "revenue": 3072.3,
        },
        {
            "date": datetime.date(2024, 1, 12),
            "product_id": "P001",
            "product_name": "Product 1",
            "quantity": 310,
            "revenue": 18900.7,
        },
        {
            "date": datetime.date(2024, 1, 12),
            "product_id": "P002",
            "product_name": "Product 2",
            "quantity": 80,
            "revenue": 2827.2,
        },
        {
            "date": datetime.date(2024, 1, 12),
            "product_id": "P003",
            "product_name": "Product 3",
            "quantity": 108,
            "revenue": 8762.04,
        },
        {
            "date": datetime.date(2024, 1, 12),
            "product_id": "P004",
            "product_name": "Product 4",
            "quantity": 143,
            "revenue": 6938.36,
        },
        {
            "date": datetime.date(2024, 1, 12),
            "product_id": "P005",
            "product_name": "Product 5",
            "quantity": 342,
            "revenue": 9216.9,
        },
        {
            "date": datetime.date(2024, 1, 13),
            "product_id": "P001",
            "product_name": "Product 1",
            "quantity": 302,
            "revenue": 18412.94,
        },
        {
            "date": datetime.date(2024, 1, 13),
            "product_id": "P002",
            "product_name": "Product 2",
            "quantity": 68,
            "revenue": 2403.12,
        },
        {
            "date": datetime.date(2024, 1, 13),
            "product_id": "P003",
            "product_name": "Product 3",
            "quantity": 96,
            "revenue": 7788.48,
        },
        {
            "date": datetime.date(2024, 1, 13),
            "product_id": "P004",
            "product_name": "Product 4",
            "quantity": 130,
            "revenue": 6307.6,
        },
        {
            "date": datetime.date(2024, 1, 13),
            "product_id": "P005",
            "product_name": "Product 5",
            "quantity": 103,
            "revenue": 2775.85,
        },
        {
            "date": datetime.date(2024, 1, 14),
            "product_id": "P001",
            "product_name": "Product 1",
            "quantity": 305,
            "revenue": 18595.85,
        },
        {
            "date": datetime.date(2024, 1, 14),
            "product_id": "P002",
            "product_name": "Product 2",
            "quantity": 84,
            "revenue": 2968.56,
        },
        {
            "date": datetime.date(2024, 1, 14),
            "product_id": "P003",
            "product_name": "Product 3",
            "quantity": 99,
            "revenue": 8031.87,
        },
        {
            "date": datetime.date(2024, 1, 14),
            "product_id": "P004",
            "product_name": "Product 4",
            "quantity": 167,
            "revenue": 8102.84,
        },
        {
            "date": datetime.date(2024, 1, 14),
            "product_id": "P005",
            "product_name": "Product 5",
            "quantity": 104,
            "revenue": 2802.8,
        },
        {
            "date": datetime.date(2024, 1, 15),
            "product_id": "P001",
            "product_name": "Product 1",
            "quantity": 301,
            "revenue": 18351.97,
        },
        {
            "date": datetime.date(2024, 1, 15),
            "product_id": "P002",
            "product_name": "Product 2",
            "quantity": 73,
            "revenue": 2579.82,
        },
        {
            "date": datetime.date(2024, 1, 15),
            "product_id": "P003",
            "product_name": "Product 3",
            "quantity": 89,
            "revenue": 7220.57,
        },
        {
            "date": datetime.date(2024, 1, 15),
            "product_id": "P004",
            "product_name": "Product 4",
            "quantity": 126,
            "revenue": 6113.52,
        },
        {
            "date": datetime.date(2024, 1, 15),
            "product_id": "P005",
            "product_name": "Product 5",
            "quantity": 100,
            "revenue": 2695.0,
        },
        {
            "date": datetime.date(2024, 1, 16),
            "product_id": "P001",
            "product_name": "Product 1",
            "quantity": 226,
            "revenue": 13779.22,
        },
        {
            "date": datetime.date(2024, 1, 16),
            "product_id": "P002",
            "product_name": "Product 2",
            "quantity": 80,
            "revenue": 2827.2,
        },
        {
            "date": datetime.date(2024, 1, 16),
            "product_id": "P003",
            "product_name": "Product 3",
            "quantity": 83,
            "revenue": 6733.79,
        },
        {
            "date": datetime.date(2024, 1, 16),
            "product_id": "P004",
            "product_name": "Product 4",
            "quantity": 175,
            "revenue": 8491.0,
        },
        {
            "date": datetime.date(2024, 1, 16),
            "product_id": "P005",
            "product_name": "Product 5",
            "quantity": 125,
            "revenue": 3368.75,
        },
    ]
    if products:
        return [item for item in data if item["product_id"] in products]
    return data


def get_promotions_data() -> List[Dict[str, Any]]:
    import datetime

    data = [
        {
            "promotion_id": "PROMO001",
            "name": "Weekend Special",
            "discount": "10% off",
            "products": ["P002"],
            "start_date": datetime.date(2024, 1, 12),
            "end_date": datetime.date(2024, 1, 14),
        },
        {
            "promotion_id": "PROMO002",
            "name": "Flash Sale",
            "discount": "15% off",
            "products": ["P001", "P003", "P005"],
            "start_date": datetime.date(2024, 1, 15),
            "end_date": datetime.date(2024, 1, 16),
        },
    ]
    return data


def get_weather_data() -> List[Dict[str, Any]]:
    data = [
        {
            "date": "2024-01-10",
            "temperature": {"fahrenheit": 23.4, "celsius": -4.8},
            "conditions": {
                "main": "Clear",
                "precipitation": "None",
                "precipitation_amount": 0,
                "special_event": None,
            },
        },
        {
            "date": "2024-01-11",
            "temperature": {"fahrenheit": 39.3, "celsius": 4.1},
            "conditions": {
                "main": "Clear",
                "precipitation": "None",
                "precipitation_amount": 0,
                "special_event": None,
            },
        },
        {
            "date": "2024-01-12",
            "temperature": {"fahrenheit": 41.1, "celsius": 5.1},
            "conditions": {
                "main": "Heavy Rain",
                "precipitation": "Heavy Rain",
                "precipitation_amount": 2.7,
                "special_event": "Flood Warning",
            },
        },
        {
            "date": "2024-01-13",
            "temperature": {"fahrenheit": 27.2, "celsius": -2.6},
            "conditions": {
                "main": "Clear",
                "precipitation": "None",
                "precipitation_amount": 0,
                "special_event": None,
            },
        },
        {
            "date": "2024-01-14",
            "temperature": {"fahrenheit": 22.9, "celsius": -5.1},
            "conditions": {
                "main": "Clear",
                "precipitation": "None",
                "precipitation_amount": 0,
                "special_event": None,
            },
        },
        {
            "date": "2024-01-15",
            "temperature": {"fahrenheit": 33.2, "celsius": 0.7},
            "conditions": {
                "main": "Clear",
                "precipitation": "None",
                "precipitation_amount": 0,
                "special_event": "High Winds",
            },
        },
        {
            "date": "2024-01-16",
            "temperature": {"fahrenheit": 23.3, "celsius": -4.8},
            "conditions": {
                "main": "Clear",
                "precipitation": "None",
                "precipitation_amount": 0,
                "special_event": None,
            },
        },
    ]
    return data


def get_competitor_pricing_data():
    data = [
        {
            "product": "Product 1",
            "date": "2024-01-10",
            "our_price": 60.97,
            "competitor_sales": {},
            "competitor_a_price": 56.88,
            "competitor_b_price": 62.23,
            "competitor_c_price": 51.8,
        },
        {
            "product": "Product 1",
            "date": "2024-01-11",
            "our_price": 60.97,
            "competitor_sales": {},
            "competitor_a_price": 59.65,
            "competitor_b_price": 72.47,
            "competitor_c_price": 72.5,
        },
        {
            "product": "Product 1",
            "date": "2024-01-12",
            "our_price": 60.97,
            "competitor_sales": {
                "CompetitorB": {
                    "original_price": 69.24,
                    "sale_price": 50.55,
                    "discount_percentage": 27,
                },
                "CompetitorC": {
                    "original_price": 49.92,
                    "sale_price": 39.44,
                    "discount_percentage": 21,
                },
            },
            "competitor_a_price": 65.4,
            "competitor_b_price": 50.55,
            "competitor_c_price": 39.44,
        },
        {
            "product": "Product 1",
            "date": "2024-01-13",
            "our_price": 60.97,
            "competitor_sales": {},
            "competitor_a_price": 72.13,
            "competitor_b_price": 57.54,
            "competitor_c_price": 51.1,
        },
        {
            "product": "Product 1",
            "date": "2024-01-14",
            "our_price": 60.97,
            "competitor_sales": {},
            "competitor_a_price": 72.36,
            "competitor_b_price": 70.04,
            "competitor_c_price": 61.04,
        },
        {
            "product": "Product 1",
            "date": "2024-01-15",
            "our_price": 60.97,
            "competitor_sales": {},
            "competitor_a_price": 68.52,
            "competitor_b_price": 59.63,
            "competitor_c_price": 73.03,
        },
        {
            "product": "Product 1",
            "date": "2024-01-16",
            "our_price": 60.97,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 53.84,
                    "sale_price": 44.69,
                    "discount_percentage": 17,
                }
            },
            "competitor_a_price": 44.69,
            "competitor_b_price": 57.69,
            "competitor_c_price": 70.51,
        },
        {
            "product": "Product 2",
            "date": "2024-01-10",
            "our_price": 35.34,
            "competitor_sales": {},
            "competitor_a_price": 34.57,
            "competitor_b_price": 42.01,
            "competitor_c_price": 42.02,
        },
        {
            "product": "Product 2",
            "date": "2024-01-11",
            "our_price": 35.34,
            "competitor_sales": {
                "CompetitorB": {
                    "original_price": 40.13,
                    "sale_price": 29.29,
                    "discount_percentage": 27,
                },
                "CompetitorC": {
                    "original_price": 28.93,
                    "sale_price": 22.85,
                    "discount_percentage": 21,
                },
            },
            "competitor_a_price": 37.91,
            "competitor_b_price": 29.29,
            "competitor_c_price": 22.85,
        },
        {
            "product": "Product 2",
            "date": "2024-01-12",
            "our_price": 35.34,
            "competitor_sales": {},
            "competitor_a_price": 41.81,
            "competitor_b_price": 33.35,
            "competitor_c_price": 29.62,
        },
        {
            "product": "Product 2",
            "date": "2024-01-13",
            "our_price": 35.34,
            "competitor_sales": {},
            "competitor_a_price": 41.94,
            "competitor_b_price": 40.6,
            "competitor_c_price": 35.38,
        },
        {
            "product": "Product 2",
            "date": "2024-01-14",
            "our_price": 35.34,
            "competitor_sales": {},
            "competitor_a_price": 39.71,
            "competitor_b_price": 34.56,
            "competitor_c_price": 42.33,
        },
        {
            "product": "Product 2",
            "date": "2024-01-15",
            "our_price": 35.34,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 31.21,
                    "sale_price": 25.9,
                    "discount_percentage": 17,
                }
            },
            "competitor_a_price": 25.9,
            "competitor_b_price": 33.44,
            "competitor_c_price": 40.87,
        },
        {
            "product": "Product 2",
            "date": "2024-01-16",
            "our_price": 35.34,
            "competitor_sales": {},
            "competitor_a_price": 33.86,
            "competitor_b_price": 28.92,
            "competitor_c_price": 41.03,
        },
        {
            "product": "Product 3",
            "date": "2024-01-10",
            "our_price": 81.13,
            "competitor_sales": {
                "CompetitorB": {
                    "original_price": 92.14,
                    "sale_price": 67.26,
                    "discount_percentage": 27,
                },
                "CompetitorC": {
                    "original_price": 66.42,
                    "sale_price": 52.47,
                    "discount_percentage": 21,
                },
            },
            "competitor_a_price": 87.02,
            "competitor_b_price": 67.26,
            "competitor_c_price": 52.47,
        },
        {
            "product": "Product 3",
            "date": "2024-01-11",
            "our_price": 81.13,
            "competitor_sales": {},
            "competitor_a_price": 95.98,
            "competitor_b_price": 76.56,
            "competitor_c_price": 68.0,
        },
        {
            "product": "Product 3",
            "date": "2024-01-12",
            "our_price": 81.13,
            "competitor_sales": {},
            "competitor_a_price": 96.29,
            "competitor_b_price": 93.2,
            "competitor_c_price": 81.22,
        },
        {
            "product": "Product 3",
            "date": "2024-01-13",
            "our_price": 81.13,
            "competitor_sales": {},
            "competitor_a_price": 91.17,
            "competitor_b_price": 79.35,
            "competitor_c_price": 97.18,
        },
        {
            "product": "Product 3",
            "date": "2024-01-14",
            "our_price": 81.13,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 71.64,
                    "sale_price": 59.46,
                    "discount_percentage": 17,
                }
            },
            "competitor_a_price": 59.46,
            "competitor_b_price": 76.76,
            "competitor_c_price": 93.83,
        },
        {
            "product": "Product 3",
            "date": "2024-01-15",
            "our_price": 81.13,
            "competitor_sales": {},
            "competitor_a_price": 77.73,
            "competitor_b_price": 66.39,
            "competitor_c_price": 94.19,
        },
        {
            "product": "Product 3",
            "date": "2024-01-16",
            "our_price": 81.13,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 80.32,
                    "sale_price": 63.45,
                    "discount_percentage": 21,
                }
            },
            "competitor_a_price": 63.45,
            "competitor_b_price": 87.76,
            "competitor_c_price": 81.93,
        },
        {
            "product": "Product 4",
            "date": "2024-01-10",
            "our_price": 48.52,
            "competitor_sales": {},
            "competitor_a_price": 57.4,
            "competitor_b_price": 45.79,
            "competitor_c_price": 40.67,
        },
        {
            "product": "Product 4",
            "date": "2024-01-11",
            "our_price": 48.52,
            "competitor_sales": {},
            "competitor_a_price": 57.59,
            "competitor_b_price": 55.74,
            "competitor_c_price": 48.58,
        },
        {
            "product": "Product 4",
            "date": "2024-01-12",
            "our_price": 48.52,
            "competitor_sales": {},
            "competitor_a_price": 54.52,
            "competitor_b_price": 47.45,
            "competitor_c_price": 58.12,
        },
        {
            "product": "Product 4",
            "date": "2024-01-13",
            "our_price": 48.52,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 42.85,
                    "sale_price": 35.57,
                    "discount_percentage": 17,
                }
            },
            "competitor_a_price": 35.57,
            "competitor_b_price": 45.91,
            "competitor_c_price": 56.11,
        },
        {
            "product": "Product 4",
            "date": "2024-01-14",
            "our_price": 48.52,
            "competitor_sales": {},
            "competitor_a_price": 46.49,
            "competitor_b_price": 39.7,
            "competitor_c_price": 56.33,
        },
        {
            "product": "Product 4",
            "date": "2024-01-15",
            "our_price": 48.52,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 48.04,
                    "sale_price": 37.95,
                    "discount_percentage": 21,
                }
            },
            "competitor_a_price": 37.95,
            "competitor_b_price": 52.48,
            "competitor_c_price": 49.0,
        },
        {
            "product": "Product 4",
            "date": "2024-01-16",
            "our_price": 48.52,
            "competitor_sales": {
                "CompetitorB": {
                    "original_price": 50.93,
                    "sale_price": 45.84,
                    "discount_percentage": 10,
                },
                "CompetitorC": {
                    "original_price": 51.01,
                    "sale_price": 40.3,
                    "discount_percentage": 21,
                },
            },
            "competitor_a_price": 41.82,
            "competitor_b_price": 45.84,
            "competitor_c_price": 40.3,
        },
        {
            "product": "Product 5",
            "date": "2024-01-10",
            "our_price": 26.95,
            "competitor_sales": {},
            "competitor_a_price": 31.99,
            "competitor_b_price": 30.96,
            "competitor_c_price": 26.98,
        },
        {
            "product": "Product 5",
            "date": "2024-01-11",
            "our_price": 26.95,
            "competitor_sales": {},
            "competitor_a_price": 30.29,
            "competitor_b_price": 26.36,
            "competitor_c_price": 32.28,
        },
        {
            "product": "Product 5",
            "date": "2024-01-12",
            "our_price": 26.95,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 23.8,
                    "sale_price": 19.75,
                    "discount_percentage": 17,
                }
            },
            "competitor_a_price": 19.75,
            "competitor_b_price": 25.5,
            "competitor_c_price": 31.17,
        },
        {
            "product": "Product 5",
            "date": "2024-01-13",
            "our_price": 26.95,
            "competitor_sales": {},
            "competitor_a_price": 25.82,
            "competitor_b_price": 22.05,
            "competitor_c_price": 31.29,
        },
        {
            "product": "Product 5",
            "date": "2024-01-14",
            "our_price": 26.95,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 26.68,
                    "sale_price": 21.08,
                    "discount_percentage": 21,
                }
            },
            "competitor_a_price": 21.08,
            "competitor_b_price": 29.15,
            "competitor_c_price": 27.21,
        },
        {
            "product": "Product 5",
            "date": "2024-01-15",
            "our_price": 26.95,
            "competitor_sales": {
                "CompetitorB": {
                    "original_price": 28.29,
                    "sale_price": 25.46,
                    "discount_percentage": 10,
                },
                "CompetitorC": {
                    "original_price": 28.33,
                    "sale_price": 22.38,
                    "discount_percentage": 21,
                },
            },
            "competitor_a_price": 23.23,
            "competitor_b_price": 25.46,
            "competitor_c_price": 22.38,
        },
        {
            "product": "Product 5",
            "date": "2024-01-16",
            "our_price": 26.95,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 27.28,
                    "sale_price": 24.01,
                    "discount_percentage": 12,
                },
                "CompetitorB": {
                    "original_price": 24.9,
                    "sale_price": 19.42,
                    "discount_percentage": 22,
                },
                "CompetitorC": {
                    "original_price": 30.56,
                    "sale_price": 23.53,
                    "discount_percentage": 23,
                },
            },
            "competitor_a_price": 24.01,
            "competitor_b_price": 19.42,
            "competitor_c_price": 23.53,
        },
    ]
    return data


def print_in_box(text, title="", cols=100, tab_level=0):
    """
    Prints the given text in a box with the specified title and dimensions.

    Args:
        text: The text to print in the box.
        title: The title of the box.
        cols: The width of the box.
        tab_level: The level of indentation for the box.
    """
    import textwrap

    text = str(text)

    # Make a box using extended ASCII characters
    if cols < 4 + tab_level * SINGLE_TAB_LEVEL:
        cols = 4 + tab_level * SINGLE_TAB_LEVEL

    tabs = " " * tab_level * SINGLE_TAB_LEVEL

    top = (
            tabs
            + "\u2554"
            + "\u2550" * (cols - 2 - tab_level * SINGLE_TAB_LEVEL)
            + "\u2557"
    )
    if tab_level == 0:
        print()  # Print a newline before any box at level 0

    if title:
        # replace the middle of the top with the title
        title = "[ " + title + " ]"
        top = top[: (cols - len(title)) // 2] + title + top[(cols + len(title)) // 2:]
    print(top)

    for line in text.split("\n"):
        for wrapped_line in textwrap.wrap(
                line, cols - 4 - tab_level * SINGLE_TAB_LEVEL
        ):
            print(
                f"{tabs}\u2551 {wrapped_line:<{cols - 4 - tab_level * SINGLE_TAB_LEVEL}} \u2551"
            )

    print(
        f"{tabs}\u255a"
        + "\u2550" * (cols - 2 - tab_level * SINGLE_TAB_LEVEL)
        + "\u255d"
    )


def safe_eval(expr):
    """
    Evaluate a mathematical expression safely.

    We normally don't want to use eval() because it can execute arbitrary code, unless we are in a
    properly sandboxed environment. This function is a safe alternative for evaluating mathematical
    expressions.
    """
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
    }

    def eval_node(node):
        """
        Recursively evaluates an AST node representing a mathematical expression.

        Args:
            node: An AST node (e.g., ast.Constant, ast.BinOp, ast.UnaryOp, ast.Expr).

        Returns:
            The evaluated result as a number (int or float).

        Raises:
            TypeError: If the node type is not supported.
        """
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            return operators[type(node.op)](eval_node(node.left), eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            return operators[type(node.op)](eval_node(node.operand))
        elif isinstance(node, ast.Expr):
            return eval_node(node.value)
        else:
            raise TypeError(f"Unsupported type: {type(node)}")

    result = eval_node(ast.parse(expr, mode="eval").body)

    if isinstance(result, float):
        return round(result, 2)
    elif isinstance(result, int):
        return result
    else:
        raise RuntimeError(f"Unsupported result type: {type(result)}")


def calculator(expression: str) -> float:
    """
    Evaluate a mathematical expression safely.
    """
    return float(safe_eval(expression))


def call_weather_api(date: str) -> Dict[str, Any]:
    data = get_weather_data()

    data = {item["date"]: item for item in data}
    return data[date]


def get_observation_message(response: str) -> str:
    """
    Take a THINK/ACT response, run the tool call, and return the observation message.

    Args:
        response (str): The THINK/ACT response.

    Returns:
        str: The observation message.

    Uses regular expressions to match the tool call and run the corresponding tool.

    If the response is invalid, return an error message as a string that the agent can understand.
    """
    from ast import literal_eval

    observation_message = None

    SALES_DATA_REGEX = r"get_sales_data\(\)"
    WEATHER_REGEX = r"call_weather_api\(date=\"(.*)\"\)"
    CALCULATOR_REGEX = r"calculator\(expression=\"(.*)\"\)"
    FINAL_ANSWER_REGEX = r"final_answer\(amount_after_spike=\"(.*)\", causes=(.*), date=\"(.*)\", percentage_spike=\"(.*)\"\)"

    # TOOL 1: get_sales_data
    if re.search(SALES_DATA_REGEX, response):
        sales_data = get_sales_data(products=["P005"])
        # filter sales data to Product 5
        sales_data = [
            item for item in sales_data if item["product_name"] == "Product 5"
        ]
        observation_message = f"OBSERVE:\n{sales_data}"

    # TOOL 2: call_weather_api
    elif re.search(WEATHER_REGEX, response):
        date = re.search(WEATHER_REGEX, response).groups()[0]
        weather_data = call_weather_api(date)
        observation_message = f"OBSERVE:\n{weather_data}"

    # TOOL 3: calculator
    elif re.search(CALCULATOR_REGEX, response):
        expression = re.search(CALCULATOR_REGEX, response).groups()[0]
        observation_message = f"OBSERVE:\n{calculator(expression)}"

    # TOOL 4: final_answer
    elif re.search(FINAL_ANSWER_REGEX, response):
        amount_after_spike, causes, date, percentage_spike = re.search(
            FINAL_ANSWER_REGEX,
            response,
        ).groups()
        causes = literal_eval(causes)
        observation_message = f"OBSERVE:\namount_after_spike: {amount_after_spike}\ndate: {date}\npercentage_spike: {percentage_spike}\ncauses: {causes}"

    # Error
    else:
        observation_message = "OBSERVE:\nInvalid tool call or tool not supported."

    return observation_message


def main():
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)

    sales_data = get_sales_data()
    sales_df = pd.DataFrame(sales_data)

    promotions_data = get_promotions_data()
    promotions_df = pd.DataFrame(promotions_data)

    weather_data = get_weather_data()
    weather_df = pd.DataFrame(weather_data)

    competitor_pricing_data = get_competitor_pricing_data()
    competitor_pricing_df = pd.DataFrame(competitor_pricing_data)

    sales_df = sales_df.sort_values(by=["product_id", "date"]).reset_index(drop=True)

    # Create a ReACT prompt that can call tools

    react_system_prompt = """
You are a meticulous Retail Demand Analyst that can solve any TASK in a multi-step process using tool calls and reasoning.

## Instructions:
- You will use step-by-step reasoning by
    - THINKING the next steps to take to complete the task and what next tool call to take to get one step closer to the final answer
    - ACTING on the single next tool call to take
- You will always respond with a single THINK/ACT message of the following format:
THINK: 
[Carry out any reasoning needed to solve the problem not requiring a tool call]
[Conclusion about what next tool call to take based on what data is needed and what tools are available]
ACT: 
[Tool to use and argument]
- As soon as you know the final answer, call the `final_answer` tool in an `ACT` message.
- ALWAYS provide a tool call, after ACT:, else you will fail.

## Available Tools
* `calculator(expression: str)`: Perform an arithmetic calculation
- Example:
    - Input: `ACT: calculator(expression="(10 + 20) / 2.0")`
    - Output: `OBSERVE: 15.0`
* `get_sales_data()`: Get the sales data
    - Example:
        - Input: `ACT: get_sales_data()`
        - Output: `OBSERVE: {"date": "2024-01-10", "product_id": "P001", "product_name": "Product 1", "quantity": 255, "revenue": 15547.35}`
* `call_weather_api(date: str)`: Get weather data for a specific date. Call this for the date of each spike.
    - Example:
        - Input: `ACT: call_weather_api(date="2024-01-10")`
        - Output: `OBSERVE: {"date": "2024-01-10", "weather": "Sunny", "temperature": 72}`

* `final_answer(amount_after_spike: str, causes: list[str], date: str, percentage_spike: str)`: Return the final answer
    - Example:
        - Input: `ACT: final_answer(amount_after_spike="32", causes=["Competitor X offering a 29 discount boosting category interest", ...], date="2020-06-12", percentage_spike="20.00%")`
        - Output: `OBSERVE: {"amount_after_spike": "32", "causes": ["Competitor X offering a 29 discount boosting category interest", ...], "date": "2020-06-12", "percentage_spike": "20.00%"}`

You will not use any other tools. Keep tools arguments in the same line.

Example:

```
--USER MESSAGE--
TASK:
Respond to the query "What was the weather one week ago?". Today is 2024-01-17.

--ASSISTANT MESSAGE--
THINK:
* I need to calculate the date one week ago from 2024-01-17.
* If today is 2024-01-17, then 7 days ago is 2024-01-10.
* I can call the `call_weather_api` tool to get the weather data for 2024-01-10.
* After that, if I have the weather data, I can return the final answer using the `final_answer` tool.
* Tool call needed: Call the `call_weather_api` tool for 2024-01-10.
ACT:
call_weather_api(date="2024-01-10")

--USER MESSAGE--
OBSERVE:
{"date": "2024-01-10", "weather": "Sunny"}

--ASSISTANT MESSAGE--
THINK:
* I have the weather data for 2024-01-10.
* I can return the final answer using the `final_answer` tool.
* Tool call needed: Call the `final_answer` tool with the weather data.   
ACT:
final_answer("The weather on 2024-01-10 was sunny.")

--USER MESSAGE--
OBSERVE:
The weather on 2024-01-10 was sunny.
```
    """

    user_prompt_analyze = """
TASK: Find the single largest sales spike according to the percentage increase with a short explanation for it based on factors such as weather.
    """

    print(f"Sending prompt to {MODEL} model...")

    # messages = [{"role": "system", "content": react_system_prompt}, {"role": "user", "content": user_prompt_analyze}]

    # react_response = get_completion(client, react_system_prompt, user_prompt_analyze)
    #
    # messages.append({"role": "assistant", "content": react_response})
    # print("Response received!\n")
    #
    # for message in messages:
    #     if message["role"] == "system":
    #         continue
    #     print_in_box(message["content"], title=f"{message['role'].capitalize()}")
    #
    # assert "ACT:" in messages[-1]["content"], (
    #     " ❌ No ACT message found in response. Looking for: \n\n ACT:"
    # )

    # assert (actual := calculator("10 + 10")) == 20.0, f" ❌ Expected 20.0, got {actual}"

    assert (
               actual := get_observation_message("""
THINK:
[thinking here]
ACT:
get_sales_data()
    """)
           ) == (expected := "OBSERVE:\n" + str(get_sales_data(products=["P005"]))), (
        f"{actual} != {expected}"
    )

    assert (
               actual := get_observation_message("""
THINK:
[thinking here]
ACT:
call_weather_api(date="2024-01-12")
    """)
           ) == (expected := "OBSERVE:\n" + str(call_weather_api("2024-01-12"))), (
        f"{actual} != {expected}"
    )

    assert (
               actual := get_observation_message("""
THINK:
[thinking here]
ACT:
final_answer(amount_after_spike="10", causes=["cause1", "cause2"], date="2024-01-12", percentage_spike="10%")
    """)
           ) == (
               expected
               := "OBSERVE:\namount_after_spike: 10\ndate: 2024-01-12\npercentage_spike: 10%\ncauses: ['cause1', 'cause2']"
           ), f"{actual} != {expected}"

    assert (
               actual := get_observation_message("""
THINK:
[thinking here]
ACT:
calculator(expression="10 + 10")
    """)
           ) == (expected := "OBSERVE:\n20.0"), f"{actual} != {expected}"

    assert (
               actual := get_observation_message("""
THINK:
[thinking here]
ACT:
invalid_tool()
    """)
           ) == (expected := "OBSERVE:\nInvalid tool call or tool not supported."), (
        f"{actual} != {expected}"
    )

    assert (
               actual := get_observation_message("""
THINK:
[thinking here]
ACT_TYPO:
get_sales_dataa()
    """)
           ) == (expected := "OBSERVE:\nInvalid tool call or tool not supported."), (
        f"{actual} != {expected}"
    )

    # create a ReACT loop
    messages = [{"role": "system", "content": react_system_prompt}, {"role": "user", "content": user_prompt_analyze}]

    for message in messages:
        if message["role"] == "system":
            continue
        print_in_box(message["content"], title=f"{message['role'].capitalize()}")

    num_react_steps = 0

    observation_message = None
    while True:

        react_response = get_completion_v2(client, messages, MODEL)
        observation_message = get_observation_message(react_response)

        messages.append({"role": "assistant", "content": react_response})

        print_in_box(
            react_response, title=f"Assistant (Think + Act). Step {num_react_steps + 1}"
        )

        messages.append({"role": "user", "content": observation_message})

        if "ACT:\nfinal_answer" in react_response:
            print_in_box(observation_message, title="FINAL ANSWER")
            break

        print_in_box(
            observation_message, title=f"User (Observe). Step {num_react_steps + 1}"
        )

        num_react_steps += 1
        if num_react_steps > 10:
            print("ERROR: Max number of React steps exceeded. Breaking.")
            break

    assert "date: 2024-01-12" in observation_message, "ReACT Loop did not find the spike date"
    assert "percentage_spike: 200" in observation_message, "ReACT Loop did not find the spike percentage increase"


if __name__ == '__main__':
    main()
