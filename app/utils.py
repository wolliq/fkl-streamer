def strtobool(val: str) -> bool:
    val = val.lower()
    if val in ("y", "yes", "true", "t", "on", "1"):
        return True
    elif val in ("n", "no", "false", "f", "off", "0"):
        return False
    else:
        raise ValueError(f"Invalid truth value: {val}")
