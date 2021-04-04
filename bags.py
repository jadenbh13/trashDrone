import torch
import cv2
import numpy as np
from torch.autograd import Variable
from darknet import Darknet
from util import process_result, load_images, resize_image, cv_image2tensor, transform_result
import pickle as pkl
import argparse
import math
import random
import os.path as osp
import os
import sys
from datetime import datetime
from tqdm import tqdm
from time import sleep
import threading
from testProc import callFunc, callFunc3
import serial

boxList = []

def load_classes(namesfile):
    fp = open(namesfile, "r")
    names = fp.read().split("\n")
    return names

def parse_args():
    fil = "pic.png"
    parser = argparse.ArgumentParser(description='YOLOv3 object detection')
    parser.add_argument('-i', '--input', default=fil, help='input image or directory or video')
    parser.add_argument('-t', '--obj-thresh', type=float, default=0.5, help='objectness threshold, DEFAULT: 0.5')
    parser.add_argument('-n', '--nms-thresh', type=float, default=0.4, help='non max suppression threshold, DEFAULT: 0.4')
    parser.add_argument('-o', '--outdir', default='output', help='output directory, DEFAULT: detection/')
    parser.add_argument('-v', '--video', action='store_true', default=False, help='flag for detecting a video input')
    parser.add_argument('-w', '--webcam', action='store_true',  default=False, help='flag for detecting from webcam. Specify webcam ID in the input. usually 0 for a single webcam connected')
    parser.add_argument('--cuda', action='store_true', default=False, help='flag for running on GPU')
    parser.add_argument('--no-show', action='store_true', default=False, help='do not show the detected video in real time')

    args = parser.parse_args()

    return args

def create_batches(imgs, batch_size):
    num_batches = math.ceil(len(imgs) // batch_size)
    batches = [imgs[i*batch_size : (i+1)*batch_size] for i in range(num_batches)]

    return batches

def draw_bbox(imgs, bbox, colors, classes,read_frames,output_path):
    img = imgs[int(bbox[0])]

    label = classes[int(bbox[-1])]

    confidence = int(float(bbox[6])*100)

    label = label+' '+str(confidence)+'%'

    #print(label)

    p1 = tuple(bbox[1:3].int())
    p2 = tuple(bbox[3:5].int())


    if 'privacy' in classes[int(bbox[-1])]:
            topLeft = p1
            bottomRight = p2
            x, y = topLeft[0], topLeft[1]
            w, h = bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1]

            # Grab ROI with Numpy slicing and blur
            ROI = img[y:y+h, x:x+w]
            blur = cv2.GaussianBlur(ROI, (51,51), 0)

            # Insert ROI back into image
            img[y:y+h, x:x+w] = blur
    else:

        color = colors[int(bbox[-1])]
        cv2.rectangle(img, p1, p2, color, 4)
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)[0]
        p3 = (p1[0], p1[1] - text_size[1] - 4)
        p4 = (p1[0] + text_size[0] + 4, p1[1])
        cv2.rectangle(img, p3, p4, color, -1)

        cv2.putText(img, label, p1, cv2.FONT_HERSHEY_SIMPLEX, 1, [225, 255, 255], 1)



def detect_image(model, args):
    l = 0
    sep = threading.Thread(target=callFunc, args=(1,))
    sep.start()
    while l == 0:
        try:
            #print('Loading input image(s)...')
            input_size = [int(model.net_info['height']), int(model.net_info['width'])]
            batch_size = int(model.net_info['batch'])

            imlist, imgs = load_images(args.input)
            #print('Input image(s) loaded')

            img_batches = create_batches(imgs, batch_size)

            # load colors and classes
            colors = pkl.load(open("pallete", "rb"))
            classes = load_classes("we/garb.names")
            #print(classes)

            if not osp.exists(args.outdir):
                os.makedirs(args.outdir)

            start_time = datetime.now()

            for batchi, img_batch in tqdm(enumerate(img_batches)):
                img_tensors = [cv_image2tensor(img, input_size) for img in img_batch]
                img_tensors = torch.stack(img_tensors)
                img_tensors = Variable(img_tensors)
                if args.cuda:
                    img_tensors = img_tensors.cuda()
                detections = model(img_tensors, args.cuda).cpu()
                detections = process_result(detections, args.obj_thresh, args.nms_thresh)

                ins = open("run.txt", "r")
                v = ins.read()
                print(v)

                if "Land" in v:
                    print("Break")
                    print("Break")
                    l += 1
                    break

                if len(detections) == 0:
                    print("Nothing")
                    continue

                detections = transform_result(detections, img_batch, input_size)

                for detection in detections:
                    labe = classes[int(detection[-1])]
                    con = int(float(detection[6])*100)
                    print(labe)
                    print(con)
                    boxList.append(labe)
                    #print(boxList)
                    draw_bbox(img_batch, detection, colors, classes,0,args.outdir)
                for i, img in enumerate(img_batch):
                    save_path = osp.join(args.outdir, osp.basename(imlist[batchi*batch_size + i]))
                    cv2.imwrite(save_path, img)
                    cv2.imshow("output", img)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord("q"):
                        l += 1
                        break
                    #print(save_path, 'saved')

            end_time = datetime.now()
            #print('Detection finished in %s' % (end_time - start_time))
        except Exception as e:
            print(e)

    return

def main():
    args = parse_args()

    if args.cuda and not torch.cuda.is_available():
        #print("ERROR: cuda is not available, try running on CPU")
        sys.exit(1)

    #print('Loading network...')
    model = Darknet("we/yolov3_garb_test.cfg")
    model.load_weights('we/garb.weights')
    if args.cuda:
        model.cuda()

    model.eval()
    #print('Network loaded')

    print('Detecting...')
    detect_image(model, args)



def runs():
    with open('run.txt', 'w') as filetowrite:
        filetowrite.write('Start')
    sleep(1)
    main()
    print(boxList)
    try:
        s = serial.Serial('/dev/ttyUSB0', 115200, timeout=3)
        for x in boxList:
            if x == 'Plastic_bag':
                s.write(b'0')
            elif x == 'cardboard':
                s.write(b'1')
            elif x == 'container_small':
                s.write(b'2')
    except:
        print("No serial port found")
    cv2.destroyAllWindows()
runs()
