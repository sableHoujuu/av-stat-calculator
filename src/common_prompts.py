# Contains functions for creating common user prompts


def confirm(prompt) -> bool:
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
        if answer in ("y", "yes", "n", "no"):
            return answer in ("y", "yes")
        print("Please enter y or n.")

def range(prompt, min: float, max: float) -> float:
    while True:
        answer = float(input(f"{prompt}:").strip().lower())
        if answer >= min and answer <= max:
            return answer
        print(f"Please enter a value between {min} and {max}.")
