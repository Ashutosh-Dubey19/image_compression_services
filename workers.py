from utils import compress_image
from database import products_collection

async def process_images(request_id: str):
    products = await products_collection.find({"id": request_id}).to_list(None)

    for product in products:
        output_images = []
        for url in product['input_image_urls']:
            compressed_image = compress_image(url)
            # Here you would save the compressed image to a storage service and get the URL
            output_images.append("compressed_image_url_placeholder")  # Replace with actual URL
        await products_collection.update_one(
            {"id": request_id, "serial_number": product["serial_number"]},
            {"$set": {"output_image_urls": output_images, "status": "Completed"}}
        )
