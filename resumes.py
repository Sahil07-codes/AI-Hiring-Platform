import pdfplumber as pp

def resume_extractor(file_path):
    raw_text = ""
    try:
        with pp.open(file_path) as pdf:
            total_pages=len(pdf.pages)

            for i in range(total_pages):
                page = pdf.pages[i]
                text = page.extract_text() 
                raw_text += text

            if raw_text == "":
                raise ValueError("PDF has no scannable text")
        return raw_text

    except ValueError as e:
        print(e)

    except FileNotFoundError:
        print("File path is invalid")

    