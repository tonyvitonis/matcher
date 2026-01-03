# Token Matcher

This project provides a simple Python token matching language.

## Sample usage

    from matcher.matcher import Matcher

    specification = "(token1 and token2) or token3"
    matcher = Matcher(specification)

    matcher.matches(["token1", "token2"]) # True
    matcher.matches(["token3", "token4"]) # True
    matcher.matches(["token1"])           # False

    specification = "start* or *end"
    matcher = Matcher(specification)

    matcher.matches(["start"])        # True
    matcher.matches(["end"])          # True
    matcher.matches(["starting"])     # True
    matcher.matches(["dead-end"])     # True
    matcher.matches(["star", "band"]) # False
