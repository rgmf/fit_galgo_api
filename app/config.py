import os


config = {
    "COUCHBASE_CLUSTER": "172.17.0.2",
    "COUCHBASE_USERNAME": "admin",
    "COUCHBASE_PASSWORD": "123456",
    "COUCHBASE_BUCKET_NAME": "galgodb",

    "UPLOAD_FILES_FOLDER": "files",
    "UPLOAD_FIT_FILES_FOLDER": os.path.join("files", "fit")
}
