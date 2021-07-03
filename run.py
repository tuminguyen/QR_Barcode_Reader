from pyzbar.pyzbar import decode
import cv2
import os
import argparse


def init_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', '-m', choices=['stream', 'image'],
                        type=str, help='mode to detect: on stream/ on single image')
    parser.add_argument('--img', '-i',
                        type=str, help='image path')
    parser.add_argument('--rate', '-r', type=int, default=1,
                        help='Read after this number of frames')
    args = parser.parse_args()
    return vars(args)


if __name__ == '__main__':
    arguments = init_parse()
    if arguments['mode'] == 'stream':  # on stream/video
        cap = cv2.VideoCapture('/dev/video0')  # video2: usb cam | video0: laptop cam or pi cam
        cap.set(3, 1280)
        cap.set(4, 960)
        fps = cap.get(cv2.CAP_PROP_FPS)  # fps = 30
        frameCount = 0
        while True:
            frameCount += 1
            ret, frame = cap.read()
            if not ret:
                break
            if frameCount % arguments['rate'] == 0:
                for message in decode(frame):
                    # get message content
                    content = message.data.decode('utf8')
                    # draw bounding box (note: the color is BGR not RGB)
                    rect = message.rect  # tuple(left, top, width, height)
                    cv2.rectangle(frame, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (219, 252, 3), 6)
                    # write bar message content on top of bounding box126, 38, 181
                    cv2.putText(frame, content, (rect[0], rect[1] - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (219, 252, 3), 2)
            cv2.imshow('out', frame)
            k = cv2.waitKey(33)
            if k == 27:  # press ESC
                break
    else:  # on image
        img = cv2.imread(arguments['img'])
        # get image name
        name = arguments['img'].split("/")[-1]
        # resize image
        scale = 0.2  # scale of original shape
        w = int(img.shape[1] * scale)
        h = int(img.shape[0] * scale)
        img = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
        # print(decode(img))  # full of info (data, bounding box dimension, coordinates)
        for message in decode(img):
            # get message content
            content = message.data.decode('utf8')
            # draw bounding box (note: the color is BGR not RGB)
            rect = message.rect  # tuple(left, top, width, height)
            cv2.rectangle(img, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (219, 252, 3), 6)
            # write bar message content on top of bounding box126, 38, 181
            cv2.putText(img, content, (rect[0], rect[1] - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (219, 252, 3), 2)
        if not os.path.exists('out/'):
            os.mkdir('out')
        cv2.imwrite('out/{}'.format(name), img)
