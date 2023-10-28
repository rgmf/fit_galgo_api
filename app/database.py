from datetime import timedelta

from couchbase.bucket import Bucket
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions

from app.config import config


def get_bucket() -> Bucket:
    cluster: str = config["COUCHBASE_CLUSTER"]
    username: str = config["COUCHBASE_USERNAME"]
    password: str = config["COUCHBASE_PASSWORD"]
    bucket_name: str = config["COUCHBASE_BUCKET_NAME"]

    authenticator = PasswordAuthenticator(username, password)
    cluster = Cluster(f"couchbase://{cluster}", ClusterOptions(authenticator))

    cluster.wait_until_ready(timedelta(seconds=5))

    bucket: Bucket = cluster.bucket(bucket_name)

    return bucket


def get_collection():
    return get_bucket().scope("galgo").collection("test")
