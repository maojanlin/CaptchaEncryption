_Updated: Nov. 22, 2021_

# CaptchaEncryption
This is the prototype of an encryption scheme involves CAPTCHA to hinder exhaustive search attack. This is a final project of the Practical Cryptographic Systems (601.645) in 2021.

## Usage:
### Encryption
```
python3 CaptchaEncryption.py -e -k my_password -n 4 -i plain_text.txt -o encrypted.txt
```

The `my_password` is a user defined "weak" password, which will be further strengthened with images association. `CaptchaEncryption.py` hash the user key with a salt. The hash value will be divided into several indexes, the indexed images will poped up and the user should type in those associations. The associations will be hashed and XOR with the original key to generate the final key.

An AES CBC mode operation with final key will be performed on the input text file `plain_text.txt` to genereate encrypted data `encrypted.txt`.

Note: special charaters such as "ä", "ê" will be transformed into standard ASCII characters.


### Decryption
```
python3 CaptchaEncryption.py -d -k my_password -n 4 -i encrypted.txt -o decrypted_text.txt
```

The `my_password` is should be the same as encryption password. The same sequence of images will poped out. The same associations will derive the final key used in encryption. AES CBC mode will be performed to generate the `decrypted_text.txt`, which should be the same as `plain_text.txt` in encryption except special characters.
