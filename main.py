import Hello_Dad
import Hello_Mom
import Hello_GitHub

__version__ = "0.0.1"

if __name__ == "__main__":
    Hello_Dad.hello_dad()
    Hello_Mom.hello_mom()
    Hello_GitHub.hello_github()
    print("Hello Python!")
    print(f"Version: {__version__}")