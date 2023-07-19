
dev_mode = True

def debug(*args, **kwargs):
    if dev_mode:
        print(*args, **kwargs)