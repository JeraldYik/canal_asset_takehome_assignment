import os


def must_init(key: str) -> str:
    val = os.environ.get(key)
    assert val is not None
    return val


if __name__ == "__main__":
    pass
