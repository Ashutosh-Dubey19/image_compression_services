from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from utils import validate_csv
from workers import process_images
from database import products_collection
from models import ProductInDB
import uuid

router = APIRouter()

@router.post("/upload/")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8")
    try:
        products_data = validate_csv(content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    request_id = str(uuid.uuid4())

    for product_data in products_data:
        product = ProductInDB(**product_data, id=request_id)
        await products_collection.insert_one(product.dict(by_alias=True))

    background_tasks.add_task(process_images, request_id)

    return {"request_id": request_id, "status": "File uploaded successfully"}

@router.get("/status/{request_id}")
async def get_status(request_id: str):
    product = await products_collection.find_one({"id": request_id})
    if product is None:
        raise HTTPException(status_code=404, detail="Request ID not found")
    return {"request_id": request_id, "status": product["status"]}
