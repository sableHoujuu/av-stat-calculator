# Contains functions for creating common user prompts


def confirm(prompt) -> bool:
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
        if answer in ("y", "yes", "n", "no"):
            return answer in ("y", "yes")
        print("Please enter y or n.")
