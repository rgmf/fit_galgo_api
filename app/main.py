from fastapi import FastAPI

from app.routers import files

app = FastAPI()
app.include_router(files.router)


@app.get("/")
async def root():
    return {"message": "Welcome to FitGalgo API"}



# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}


# @app.post("/fit/files")
# async def fit_files(files: list[UploadFile]):
#     response: dict[str, list] = {"data": []}

#     fit_files_folder: str = os.path.join(config["UPLOAD_FIT_FILES_FOLDER"])
#     Path(fit_files_folder).mkdir(parents=True, exist_ok=True)

#     for file in files:
#         fit_file_path: str = os.path.join(fit_files_folder, file.filename)
#         with open(fit_file_path, "wb") as file_object:
#             chunk: bytes = await file.read(10_000)
#             while chunk:
#                 file_object.write(chunk)
#                 chunk: bytes = await file.read(10_000)

#         galgo: FitGalgo = FitGalgo(fit_file_path)
#         model: FitModel = galgo.parse()

#         uuid: str = str(uuid4())
#         collection = get_collection()
#         result = collection.insert(uuid, jsonable_encoder(model))
#         cas = result.cas

#         response["data"].append({
#             "filename": file.filename,
#             "document_id": uuid,
#             "cas": cas
#         })

#     return response


# @app.get("/test")
# def test():
#     collection = get_collection()
#     document: dict[str, str] = {"foo": "bar", "bar": "foo"}
#     result = collection.insert("test_1", document)
#     cas = result.cas
#     return {"hola": "amigo", "result": cas}
