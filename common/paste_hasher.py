from common.mm3 import MurmurHasher
from pastebin.models import Paste
from random import choice
from string import ascii_letters, ascii_lowercase, ascii_uppercase, digits

class PasteHasher:
    def __init__(self, seed, r_len):
        self.hasher = MurmurHasher(seed)
        self.selection = ascii_uppercase + ascii_lowercase + digits
        self.r_len = r_len
        super().__init__()

    def generate_hash(self, paste: Paste):
        s = rand_string(self.selection, self.r_len)
        key = ''.join([str(paste.creation_date), s])
        return hex(self.hasher.do32Hash(key))

def rand_string(selection, n):
    return ''.join(choice(selection) for _ in range(n))