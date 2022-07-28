def convert_hello(user_github_name: str) -> str:
    result = f"# 안녕하세요 [{user_github_name}](https://github.com/{user_github_name}) 입니다! "
    result += '<img src="https://raw.githubusercontent.com/MartinHeinz/MartinHeinz/master/wave.gif" width=50px>'
    return result


def convert_introduction(user_introduction: str) -> str:
    result = "\n\n# 💫About Me :\n"
    result += user_introduction.replace('\n', "\\\n")
    return result
