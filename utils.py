import csv
from typing import List
from io import StringIO
from PIL import Image
import requests
from io import BytesIO

def validate_csv(file_content: str) -> List[dict]:
    file = StringIO(file_content)
    reader = csv.DictReader(file)

    required_columns = ["S", "P", "I"]

    if not all(column in reader.fieldnames for column in required_columns):
        raise ValueError("CSV format is incorrect: Missing required columns")

    data = []
    for row in reader:
        data.append({
            "serial_number": int(row["S"]),
            "product_name": row["P"],
            "input_image_urls": row["I"].split(",")
        })

    return data

def compress_image(url: str) -> bytes:
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((img.width // 2, img.height // 2))
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG', quality=85)
    return output_buffer.getvalue()
