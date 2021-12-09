from captcha.image import ImageCaptcha
import random
import os
# import time
import tarfile
import multiprocessing as mp

img = ImageCaptcha(width=150, height=50)
txt = (''.join(map(lambda x:chr(x+ord('0')), range(10))) +
        ''.join(map(lambda x:chr(x+ord('a')), range(26))) +
        ''.join(map(lambda x:chr(x+ord('A')), range(26))))

def generate_cap(args):
    ind, dir = args
    out = ''.join(random.sample(txt, 5))
    image = img.generate_image(out)
    # image = img.create_noise_dots(image, 'red', width=3, number=40)
    # image = img.create_noise_curve(image, 'cyan')
    fname = f'{dir}/{ind}.png'
    image.save(fname)


def main():
    folder_name = 'captcha_bundle2'
    os.makedirs(folder_name, exist_ok=True)
    # time1 = time.time()
    #for i in range(2**8):
    #    generate_cap(i,folder_name) zip(range(2**20), itertools.repeat(folder_name))
    with mp.Pool() as pool:
        for _ in pool.imap_unordered(generate_cap, ((i, folder_name) for i in range(2**20))):
            pass
    # time2 = time.time()-time1
    # print(time2)
    with tarfile.open('captcha.tar.gz', 'w:gz') as tar:
        tar.add(folder_name)

if __name__ == '__main__':
    main()