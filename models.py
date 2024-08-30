from pydantic import BaseModel, Field
from typing import List

class ProductInDB(BaseModel):
    id: str
    serial_number: int
    product_name: str
    input_image_urls: List[str]
    output_image_urls: List[str] = Field(default_factory=list)
    status: str = "Processing"
