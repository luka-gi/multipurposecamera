import cv2
import sys
import numpy as np

def pixel (img):
    img = img.astype(np.float64) 
    pixel = lambda x,y : {
        0: [ img[x][y] , (img[x][y-1] + img[x-1][y] + img[x+1][y] + img[x][y+1]) / 4 ,  (img[x-1][y-1] + img[x+1][y-1] + img[x-1][y+1] + img[x+1][y+1]) / 4 ] ,
        1: [ (img[x-1][y] + img[x+1][y])  / 2,img[x][y] , (img[x][y-1] + img[x][y+1]) / 2 ],
        2: [(img[x][y-1] + img[x][y+1]) / 2 ,img[x][y], (img[x-1][y] + img[x+1][y]) / 2],
        3: [(img[x-1][y-1] + img[x+1][y-1] + img[x-1][y+1] + img[x+1][y+1]) / 4 , (img[x][y-1] + img[x-1][y] + img[x+1][y] + img[x][y+1]) / 4 ,img[x][y] ]
    } [  x % 2 + (y % 2)*2]
    res = np.zeros ( [    np.size(img,0) , np.size(img,1)  , 3] )
    for x in range (1,np.size(img,0)-2):
        for y in range (1,np.size(img,1)-2):
            p = pixel(x,y)
            p.reverse();
            res[x][y] = p
    res = res.astype(np.uint8)
    return res

def channel_break (img):
    img = img.astype(np.float64) 
    red=np.copy (img);red [1::2,:]=0;red[:,1::2]=0
    blue=np.copy (img);blue [0::2,:]=0;blue[:,0::2]=0
    green=np.copy (img);green [0::2,0::2]=0;green [1::2,1::2]=0;
    red = red.astype(np.float64) 
    blue = blue.astype(np.float64) 
    green = green.astype(np.float64) 
    return (red,green,blue)

def rgb2gray(img):
    res = np.zeros ( [    np.size(img,0) , np.size(img,1)  , 3] )
    res = res.astype(np.float64) 
    for x in range (1,np.size(img,0)-1):
        for y in range (1,np.size(img,1)-1):
            res[x][y]=img[x][y][0]*0 + img[x][y][1]*0.5 + img[x][y][2]*0.5;
    res = res.astype(np.uint8)
    return res

def pycam_img_cap(img_path = "./test.png"):
    cap = cv2.VideoCapture(0)
    success, img = cap.read()

    # plt.imshow(img)
    # plt.title ('bayer img')
    # plt.imsave('bayer_img.png', img)

    # img = cv2.imread(img_path)
 
    img = np.asarray(img, dtype=np.uint8)
    colour = cv2.cvtColor(img, cv2.COLOR_BAYER_GBGB2BGR)
    plt.imshow(colour)
    plt.title ('color image by open cv')
    plt.imsave('color_image_by_opencv.png', colour)

    if success:
        cv2.imwrite(img_path,img)
        print("\ncamera capture: success\n")
    else:
        print("\ncamera capture: failure\n")
    cap.release()
    return

if __name__ == "__main__":
    if len(sys.argv) == 2:
        # pycam_img_cap(sys.argv[1])
        print("\nsaving img to:" + sys.argv[1] + "\n")
    else:
        print("\nsaving img to test folder\n")
        pycam_img_cap()