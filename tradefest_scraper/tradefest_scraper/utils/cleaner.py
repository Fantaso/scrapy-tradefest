# Removes
import re


def remove_new_lines(value: str):
    return value.replace("\n", "")


def remove_hashtags(value):
    return value.replace("#", "")


def remove_first_2_chars(value: str):
    return value[2:]


def remove_empty_spaces(value):
    return value.replace(" ", "")


def remove_html_tags(value):
    return re.sub(r"<[^>]*>", " ", value).strip()


# Splits
def split_ref(value):
    return value.split("?ref")


def split_space(value):
    return value.split(" ")


def split_space_and_remove_empty_values(value):
    return [v for v in value.split(" ") if v]


def split_space_and_get_second(value):
    return split_space_and_remove_empty_values(value)[1]


def split_space_and_get_fourth(value):
    return split_space_and_remove_empty_values(value)[3]


def split_comma_and_get_penultimate(value):
    return value.split(",")[-2]


def split_open_parenthesis(value):
    return value.split("(")


# Others
def extract_data_between_parenthesis(value):
    start = value.find("(") + 1
    end = value.find(")")
    return value[start:end]


def safe_filename(value):
    """
    Some images' names contains '/'.
    Making sure when file is saved locally
    it does not create a directory if found '/'
    """
    SLASH = '/'
    if SLASH in value:
        return value.replace(SLASH, u"\u2215")
    return value
