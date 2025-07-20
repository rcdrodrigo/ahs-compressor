# Main application file
from my_module import MyClass, calculate_sum

if __name__ == "__main__":
    instance = MyClass("TestInstance")
    instance.greet()

    result = calculate_sum(5, 3)
    print(f"The sum is: {result}")
