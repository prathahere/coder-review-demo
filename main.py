from utils import divide, is_even

def main():
    print("Welcome to CodeRabbit Demo!")
    a = 10
    b = 0  # Intentional divide-by-zero
    try:
        print("Division result:", divide(a, b))
    except Exception as e:
        print("Error occurred:", e)

    for i in range(5):
        if is_even(i):
            print(f"{i} is even")
        else:
            print(f"{i} is odd")

if __name__ == "__main__":
    main()
