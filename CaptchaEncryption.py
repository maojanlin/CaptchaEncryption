import argparse
#import htslib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def display_image_and_collect_input(list_id):
    """ This function show the CAPTCHA images and take the user inputs"""
    list_input_answer = []
    for img_id in list_id:
        img = mpimg.imread("./kaggle_dataset/" + str(img_id)+'.png')
        imgplot = plt.imshow(img)
        plt.draw()
        plt.pause(0.001)
        text = input("Please give your associated text: ")
        list_input_answer.append(text)
    return list_input_answer



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--encryption', type=bool, help='specify when enctypt document')
    parser.add_argument('-d', '--decryption', type=bool, help='specify when decrypt document')
    parser.add_argument('--inkblot', type=bool, help='include one inkblot in the puzzle set')
    parser.add_argument('-n', '--puzzle', type=int, default=4, help='number of puzzles used in encryption and decryption')
    parser.add_argument('-i', '--input' , help='input document path')
    parser.add_argument('-o', '--output', help='output document path')
    args = parser.parse_args()
    
    flag_decrypt = args.decryption
    flag_encrypt = args.encryption
    flag_inkplot = args.inkblot
    num_puzzle = args.puzzle
    fn_input  = args.input
    fn_output = args.output
    
    list_input_answer = display_image_and_collect_input([15,23])
    print(list_input_answer)
