# Leon | Original learning example
# Keep a word beside its row
# Python 3.12+ | Run: python document-ocr-qa-document-row.py
words = [("Friday", (10, 40, 80, 60)), ("Room 3", (100, 40, 170, 60)), ("Room 8", (100, 80, 170, 100))]
target_y = 50
selected = []
for text, box in words:
    centre_y = (box[1] + box[3]) / 2
    if abs(centre_y - target_y) <= 5:
        selected.append((box[0], text))
selected.sort()
print("row:", [text for left, text in selected])
print("normalized x:", 1000 * 100 / 500)
