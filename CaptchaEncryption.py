import argparse
import hashlib
import random
import string

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import base64
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from Crypto import Random

global data_size
data_size = 1040

def generate_salt(seed_num):
    random.seed(seed_num)
    salt = ""
    for i in range(128):
        salt += random.choice(string.ascii_letters)
    return salt


def display_image_and_collect_input(list_id):
    """ This function shows the CAPTCHA images and take the user inputs"""
    list_input_answer = []
    for img_id in list_id:
        print("./CAPTCHA_dataset/" + str(img_id)+'.png')
        img = mpimg.imread("./CAPTCHA_dataset/" + str(img_id)+'.png')
        imgplot = plt.imshow(img)
        plt.draw()
        plt.pause(0.001)
        text = input("Please give your associated text: ")
        list_input_answer.append(text)
    return list_input_answer


def hash_and_salt(user_key_encode, salt):
    """ salt should be fixed in encryption and decryption """
    dk = hashlib.pbkdf2_hmac('sha256', user_key_encode, salt.encode(), 131072)
    #m = hashlib.sha256(user_key.encode())
    #m.update(salt.encode())
    #return m.digest() #.hexdigest()
    return dk #.hexdigest()


def round_puzzle_num(num_puzzle):
    """ round the num_puzzle to 1, 2, 4, or 8 """
    min_idx = 0
    min_diff = 100
    if abs(num_puzzle - 1) < min_diff:
        min_diff = num_puzzle - 1
        min_idx = 1
    if abs(num_puzzle - 2) < min_diff:
        min_diff = num_puzzle - 2
        min_idx = 2
    if abs(num_puzzle - 4) < min_diff:
        min_diff = num_puzzle - 4
        min_idx = 4
    if abs(num_puzzle - 8) < min_diff:
        min_diff = num_puzzle - 8
        min_idx = 8
    if num_puzzle != min_idx:
        print("number of puzzle is round to ", min_idx)
    return min_idx


class AESCipher(object):   # AES code by mnothic from stackoverflow
    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key).digest()
    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))
    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]






if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--encryption', action='store_true', help='specify when encrypt document')
    parser.add_argument('-d', '--decryption', action='store_true', help='specify when decrypt document')
    parser.add_argument('--inkblot', action='store_true', help='include one inkblot in the puzzle set')
    parser.add_argument('-n', '--puzzle', type=int, default=4, help='number of puzzles used in encryption and decryption, can only be 1, 2, 4, or 8')
    parser.add_argument('-k', '--key', help='encryption/decryption key')
    parser.add_argument('-i', '--input' , help='input document path')
    parser.add_argument('-o', '--output', help='output document path')
    args = parser.parse_args()
    
    # input all the parameters
    flag_decrypt = args.decryption
    flag_encrypt = args.encryption
    assert(flag_decrypt ^ flag_encrypt == True), "Only one of \"-e\" or \"-d\" options should be used."
    flag_inkplot = args.inkblot
    num_puzzle = args.puzzle
    num_puzzle = round_puzzle_num(num_puzzle)
    user_key  = args.key
    assert(len(user_key) > 0), "\"--key\" option should be specified!"
    fn_input  = args.input
    fn_output = args.output
    
    # generate_salt
    salt_1 = generate_salt(484872067538)
    salt_2 = generate_salt(2375892735927835)
    salt_3 = generate_salt(56279381409)


    # hash user key
    hash_key = hash_and_salt(user_key.encode(), salt_1)
    print("hash_key", hash_key)
    print("hash_key", type(hash_key), len(hash_key))
    
    
    # generate CAPTCHA indexes from the hash_key
    list_big_idx = []
    len_portion = int(32/num_puzzle)
    for idx in range(num_puzzle):
        key_portion = hash_key[idx*len_portion:(idx+1)*len_portion]
        big_portion = int.from_bytes(key_portion, "big")
        list_big_idx.append(big_portion % data_size)
    

    # perform CAPTCHA association
    print(list_big_idx)
    list_input_answer = display_image_and_collect_input(list_big_idx)
    print(list_input_answer)


    # mix user_key with CAPTCHA associations
    mix_key = hash_key
    print("mix_key", mix_key.hex())
    for associate in list_input_answer:
        hash_associate = hash_and_salt(associate.encode(), salt_2)
        mix_key = bytes(a ^ b for (a, b) in zip(mix_key, hash_associate))


    # generate final key
    final_key = hash_and_salt(mix_key, salt_3)
    print('final_key', final_key.hex())
    

    # perform AES encryption / decryption
    if flag_encrypt == True:    # encryption process
        fi = open(fn_input, 'r')
        raw_data = ""
        for ele in fi:
            raw_data += ele
        fi.close()
        
        # perform AES encryption
        cipher = AESCipher(final_key)
        encrypted_text = cipher.encrypt(raw_data)
    
        fo = open(fn_output, 'wb')
        fo.write(encrypted_text)
        fo.close()
    elif flag_decrypt == True:  # decrypt process
        with open(fn_input, 'rb') as encrypted_file:
            read_data = encrypted_file.read()

        # perform AES decryption
        cipher = AESCipher(final_key)
        decrypted_text = cipher.decrypt(read_data)
        print(decrypted_text)
    else:
        print("ERROR!, option for encryption/decryption has problems!")


