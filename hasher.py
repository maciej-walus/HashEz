import hashlib, os
def hash_password(raw_password, salt=""):
    password = raw_password.encode("utf-8")
    if salt == "":
        salt = hashlib.sha256(os.urandom(32)).digest()
    iterations = 100000
    dkeylen = 32
    hashed_password = hashlib.pbkdf2_hmac("sha256", password, salt, iterations, dkeylen)
    return hashed_password, salt
