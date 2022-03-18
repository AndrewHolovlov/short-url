from hashids import Hashids


def get_token(url: str):
    hashids = Hashids(salt=url, min_length=7)
    return hashids.encode(1)
