index = 10
print(index)

price = 10.50
print(price)

price_from_text = float("5.95")
print(price_from_text + 1.55)

index_of_page = "3"
print(int(index_of_page) + 2)

actual_prices: list[float] = [5.95, 10.50, 3.05]
print(actual_prices)
print(max(actual_prices))


def is_first_price_the_highest(target_prices: list[float]):
    return target_prices[1] == max(target_prices)


print(is_first_price_the_highest(actual_prices))

actual_prices.sort()
print(actual_prices)

actual_prices.sort(reverse=True)
print(actual_prices)
