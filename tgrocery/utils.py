# TODO how to realize more elegantly?
def read_text_src(text_src):
    if isinstance(text_src, str):
        with open(text_src, 'r') as f:
            text_src = [line.split('\t') for line in f]
    elif not isinstance(text_src, list):
        raise TypeError('text_src should be list or str')
    return text_src
