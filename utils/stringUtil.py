import re


def remove_urls_clean(text):
    """
    删除URL并清除多余空格
    :param text:
    :return:
    """
    # 删除URL
    no_urls = re.sub(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.\-?=%&:#@$,;+!]*', '', text)
    # 清除连续空格和空行
    return re.sub(r'\s+', ' ', no_urls.strip())


def remove_all_tags(text):
    """
        删除所有HTML标签（如 <a>、<span> 等）
        :param text:
        :return:
        """
    # 匹配所有 HTML 标签
    return re.sub(r'<[^>]+>', '', text)


def clean_string(text):
    text = remove_urls_clean(text)
    text = remove_all_tags(text)
    # 匹配所有中文字符（含扩展区）、数字、大小写字母
    pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\U00020000-\U0002a6dfa-zA-Z0-9]')
    return "".join(pattern.findall(text))
