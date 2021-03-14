import hashlib
def md5sum(filename, blocksize=65536):
    return checksum(filename, hashlib.md5(), blocksize)

def sha256sum(filename, blocksize=65536):
    return checksum(filename, hashlib.sha256(), blocksize)

def checksum(filename, hash, blocksize=65536):
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()