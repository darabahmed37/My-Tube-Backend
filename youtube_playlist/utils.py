def check_tag(tag1: str, tag2: str):
    tag1 = tag1.lower()
    tag2 = tag2.lower()
    if tag1 in tag2:
        return tag1
    elif tag2 in tag1:
        return tag2
    else:
        return None


def compare_tags(tag: str, tags: list[str]):
    for t in tags:
        output = check_tag(tag, t)
        if output is not None:
            return output
    return None
