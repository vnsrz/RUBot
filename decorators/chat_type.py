def private(fn):
    def wrapper(*args, **kwargs):
        message = args[0].message

        if message.chat.type == 'private':
            return fn(*args, **kwargs)
        else:
            return False

    return wrapper

def group(fn):
    def wrapper(*args, **kwargs):
        message = args[0].message

        if message.chat.type == 'group' or message.chat.type == 'supergroup':
            return fn(*args, **kwargs)
        else:
            return False

    return wrapper