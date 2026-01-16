def replace_self_from_attr_name(attr: str) -> str:
    new_name = attr.split("=")[0].replace("self.", "")
    return new_name[1:] if new_name.startswith("_") else new_name


if __name__ == "__main__":
    pass



