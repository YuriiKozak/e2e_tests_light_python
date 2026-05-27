hello_world: str = "Hello, World!"


def print_hello_world():
    print(hello_world)


def hello_to(name: str):
    print(f"Hello, {name}!")


print(hello_world)
print(hello_world.upper())
print(hello_world.lower())
print(hello_world.removesuffix(", World!"))
print(hello_world.removeprefix("Hello, "))

print_hello_world()
hello_to("Yurii")
