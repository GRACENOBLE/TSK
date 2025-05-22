import typer
from enum import Enum

class GreetingType(str, Enum):
    formal = "formal"
    informal = "informal"

app = typer.Typer()

@app.command()
def hello(name: str):
    print(f"hello {name}")

@app.command()
def goodbye(
    name: str,
    greeting_type: GreetingType = typer.Option(
        GreetingType.informal, "--greeting-type", "-g", help="Type of greeting"
    ),
):
    if greeting_type == GreetingType.formal:
        print(f"Goodbye Mr. {name}. Have a great day")
    else:
        print(f"Bye {name}")

if __name__ == "__main__":
    app()
