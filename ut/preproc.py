def preprocess_text(text, args={}):
    if '#skip_preproc' in text:
        return text

    for k, v in args.items():
        if k.startswith('{'):
            text = text.replace(k, v)

    return text


__loader__._preproc = preprocess_text
