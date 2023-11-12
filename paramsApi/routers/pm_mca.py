from fastapi import APIRouter, File, UploadFile, Request, Query
from starlette.responses import FileResponse
from .. import schemas
from ..services import pm_mca_srv
from datetime import datetime
import pytz
import os
import logging


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/pm_mca',
    tags=['pm mca']
)


@router.get('/{brand}',
            response_model=schemas.FilterResponse,
            summary="返回某个品牌的pm mca数据")
def get_pm_mca(brand: str):
    return schemas.FilterResponse(
        data=pm_mca_srv.get_pm_mca(brand)
    )


def delete_files_in_directory(directory_path: str):
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

@router.post("/upload_file",
             response_model=schemas.UploadFileResponse,
             summary="upload file...")
async def upload_file(request: Request, file: UploadFile = File(...)):
    try:
        res = await file.read()
        current_time = datetime.now()
        local_timezone = pytz.timezone('Asia/Shanghai')
        local_time = current_time.astimezone(local_timezone)
        form_data = await request.form()
        # 获取brnad数据
        brand = form_data["brand"]
        folder = ""
        if brand == '中兴':
            folder = "c:\data"  # '/data/gtj/pm/zx/zxmca/'
        elif brand == '烽火':
            folder = '/data/gtj/pm/fh/fhmca/'
        delete_files_in_directory(folder)
        temp_file = folder + 'pm_mac.xlsx'
        idx = temp_file.index(".xlsx")
        formatted_time = local_time.strftime("%Y%m%d%H%M%S")
        save_file = f"{temp_file[0:idx]}{formatted_time}.xlsx"

        with open(save_file, "wb") as f:
            f.write(res)
        return schemas.UploadFileResponse(data=None)
    except Exception as e:
        logger.exception(e)
        return schemas.UploadFileResponse(
            data="fail"
        )


@router.get("/download")
async def download_file(file_name: str = Query(...)):
    file_path = f"/data/dl/{file_name}"
    return FileResponse(file_path, filename=file_name)
