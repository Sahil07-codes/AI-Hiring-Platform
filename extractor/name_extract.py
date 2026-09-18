def name_extractor(raw_text):
    data=raw_text.split()
    return f'{data[0]} {data[1]}'