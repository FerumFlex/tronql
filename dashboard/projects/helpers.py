import random
import string


def generate_token(count: int = 30) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=count))
