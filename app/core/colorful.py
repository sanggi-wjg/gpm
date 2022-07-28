from colorful_print import color


def colorful_dispatcher(c: str, *args, **kwargs):
    dispatch = getattr(color, c)
    dispatch(*args, **kwargs)


def red(*args, **kwargs):
    colorful_dispatcher('red', *args, **kwargs)


def yellow(*args, **kwargs):
    colorful_dispatcher('yellow', *args, **kwargs)


def green(*args, **kwargs):
    colorful_dispatcher('green', *args, **kwargs)


def blue(*args, **kwargs):
    colorful_dispatcher('blue', *args, **kwargs)


def magenta(*args, **kwargs):
    colorful_dispatcher('magenta', *args, **kwargs)


def white(*args, **kwargs):
    colorful_dispatcher('white', *args, **kwargs)
