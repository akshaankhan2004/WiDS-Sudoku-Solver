import cv2 as cv
import numpy as np
import tensorflow as tf
from tensorflow import keras
from solver.sudoku_solver import SudokuSolver
from utils import *

model = keras.models.load_model('models/myModel.h5')
solver = SudokuSolver()

img = cv.imread('sudoku_img.jpeg')
img = cv.resize(img, (450,450))
blank = np.zeros((450,450,3), np.uint8)
img_threshold = preProcess(img)
contours, hierarchy = cv.findContours(img_threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
cv.drawContours(img, contours, -1, (0, 255, 0), 3)
biggest, maxArea = biggestContour(contours)

if biggest.size != 0:
    biggest = reorder(biggest)
    cv.drawContours(img, biggest, -1, (0, 0, 255), 25)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0],[450, 0], [0, 450],[450, 450]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    imgWarpColored = cv.warpPerspective(img, matrix, (450,450))
    imgDetectedDigits = blank.copy()
    imgWarpColored = cv.cvtColor(imgWarpColored,cv.COLOR_BGR2GRAY)
    imgSolvedDigits = blank.copy()
    boxes = splitBoxes(imgWarpColored)
    numbers = getPredection(boxes, model)
    sudoku = np.array(numbers).reshape(9, 9).tolist()
    solver.solveSudoku(sudoku)
    numbers = np.array(sudoku).reshape(81).tolist()
    imgDetectedDigits = displayNumbers(imgDetectedDigits, numbers, color=(255, 0, 255))

if __name__ == '__main__':
    print(sudoku)
    cv.imshow("Sudoku Solved", imgDetectedDigits)
    while True:
        if cv.waitKey(0) & 0xFF == ord('q'):
            break
    cv.destroyAllWindows()