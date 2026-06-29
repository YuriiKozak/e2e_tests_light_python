index = 10

price = 10.50

price_from_text = float("5.95")

index_of_page = "3"

actual_prices: list[float] = [5.95, 10.50, 3.05]


def is_first_price_the_highest(target_prices: list[float]):
    return target_prices[1] == max(target_prices)


actual_prices.sort()

actual_prices.sort(reverse=True)
