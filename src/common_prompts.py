# Contains functions for creating common user prompts


def confirm(prompt) -> bool:
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
        if answer in ("y", "yes", "n", "no"):
            return answer in ("y", "yes")
        print("Please enter y or n.")

def range_prompt(prompt, min: float, max: float) -> float:
    float(min)
    float(max) # python doesn't enforce types, so we cast to be sure
    while True:
        answer = float(input(f"{prompt}:").strip().lower())
        if answer >= min and answer <= max:
            return answer
        print(f"Please enter a value between {min} and {max}.") # TODO: make this print and accept more user-readable values
