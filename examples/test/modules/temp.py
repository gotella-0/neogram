import random

def get_temp(message) -> str:
    return f"{message}: {random.randint(0, 10)}"