
# dev_mode = True
dev_mode = False

def debug(*args, **kwargs):
    if dev_mode:
        print(*args, **kwargs)