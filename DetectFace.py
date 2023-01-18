import cv2

from urllib.request import urlopen

import numpy as np


def detect_face(photo_path):
    pixels = cv2.imread(photo_path)

    # Загрузка обученой модели
    classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # Выполнения распознавания лиц
    faces = classifier.detectMultiScale(pixels)
    # Формирование прямоугольников вокруг лиц
    # for box in faces:
    #     x, y, width, height = box
    #     x2, y2 = x + width, y + height
    #     cv2.rectangle(pixels, (x, y), (x2, y2), (0, 0, 255), 1)
    # cv2.imshow('Test_faces', pixels)

    # cv2.waitKey(0)
    return len(faces)


if __name__ == '__main__':
    detect_face('https://api.telegram.org/file/bot5908491217:AAFVNeJTziaDwab1aYycvHhAOQuMz6huLLM/{"file_id": "AgACAgIAAxkBAAMSY8gaBYAG0dwB1D_v9FqctHxl3RkAAmHDMRuIjEFKq0yU0EpFsGgBAAMCAAN4AAMtBA", "file_unique_id": "AQADYcMxG4iMQUp9", "file_size": 58105, "width": 650, "height": 517}')
