from werkzeug.security import check_password_hash, generate_password_hash


def check_password(hash_password, password):
    return check_password_hash(hash_password, password)


def make_hash_password(password):
    return generate_password_hash(password)


def allowed_file(filename):
    pass

def random_generator(len=8):
    pass

def get_extension(filename):
    pass