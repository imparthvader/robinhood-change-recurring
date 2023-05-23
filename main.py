from pickle import FALSE, TRUE
from numpy import take
import pyautogui
import time
import os
import sys
import glob

sys.setrecursionlimit(100)

globalConfidence = 0.8

screenshot_x = 0
screenshot_y = 0

# Check if you are on robinhood site
robinhoodImg = "Images\ACTIVE_PAGE\ROBINHOOD.png"

# For all images that you want to change freuquency FROM
baselineCheckImg = "Images\BASELINE\EVERY_WEEK.png"

baselineCheckImg1 = "Images\BASELINE\EVERY_WEEK.png"
baselineCheckImg2 = "Images\BASELINE\EVERY_2_WEEKS.png"
baselineCheckImg3 = "Images\BASELINE\EVERY_DAY.png"

# For all images that you want to change frequency TO
changeFrequencyImg = "Images\BASELINE\EVERY_MONTH.png"

# All other images in the process
baselineBottomOfPageImg = "Images\BASELINE\CHECK_BOTTOM_PAGE.png"
editInvestmentImg = "Images\PAGE_1\EDIT_INVESTMENT.png"
frequencyImg = "Images\PAGE_2\FREQUENCY.png"
reviewChangesImg = "Images\PAGE_2\REVIEW_CHANGES.png"
saveChangesImg = "Images\PAGE_2\SAVE_CHANGES.png"
backToScrollImg = "Images\PAGE_1\BACK_TO_SCROLL.png"

# Screenshot Locations
tmpScreenshots = 'Images\TEMP_SCREENSHOT'
oldScreenshots = 'Images\OLD_SCREENSHOTS'

# Number of screenshots taken
screenshotNum = 0

defaultWaitTimeSecs = 3
pyautogui.FAILSAFE = True


def defaultLoc():
    pyautogui.moveTo(100, 150)


def wait(x):
    i = 1
    while i <= x:
        print("waiting... " + str(i) + " seconds")
        time.sleep(1)
        i += 1


def scroll(Pixels):
    pyautogui.scroll(Pixels)
    print("scrolled down " + str(Pixels) + " pixels")


def typeMessage(MessageString):
    pyautogui.typewrite(MessageString, interval=0.01)


def takeScreenshot(screenshot_x, screenshot_y):
    tmp_screenshot = pyautogui.screenshot(region=(screenshot_x, screenshot_y,
                                                  400, 32))
    global screenshotNum
    screenshotNum += 1
    tmp_screenshot.save("Images\TEMP_SCREENSHOT\SCREENSHOT_" +
                        str(screenshotNum) + ".png")


def screenshotXYOffset(x, y):
    screenshot_x = x - 55
    screenshot_y = y - 40
    return screenshot_x, screenshot_y


def moveScreenshots():
    allfiles = os.listdir(tmpScreenshots)
    for f in allfiles:
        srcLoc = tmpScreenshots + "\\" + f
        destLoc = oldScreenshots + "\\" + f
        try:
            os.remove(destLoc)
        except:
            print("Could not find file in location!")
        os.rename(srcLoc, destLoc)
    print("Moved screenshots!")


def getLatestScreenshot():
    list_of_files = glob.glob(
        'Images\TEMP_SCREENSHOT\*.png'
    )  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file


def clickBaseLineImage(ImagePath, BottomOfPageImagePath, ScrollDownYPixels,
                       TakeScreenshot):
    try:
        x, y = pyautogui.locateCenterOnScreen(ImagePath,
                                              grayscale=True,
                                              confidence=globalConfidence)
        if (TakeScreenshot == TRUE):
            screenshot_x, screenshot_y = screenshotXYOffset(x, y)
            takeScreenshot(screenshot_x, screenshot_y)
        pyautogui.click(x, y)
        print("Clicked on image from path: " + str(ImagePath))
    except:
        print("Image was not found: " + str(ImagePath) + "\nScrolling down...")
        scroll(-int(ScrollDownYPixels))
        try:
            bottom_x, bottom_y = pyautogui.locateCenterOnScreen(
                BottomOfPageImagePath,
                grayscale=True,
                confidence=globalConfidence)
            if (bottom_x > 0 or bottom_y > 0):
                print(
                    "Image was not found & Bottom of page reached, skipping..."
                )
                return
        except:
            print("Bottom of page not reached, trying again...")
            clickBaseLineImage(ImagePath, BottomOfPageImagePath,
                               ScrollDownYPixels, TakeScreenshot)


def clickMultiBaseLineImage(ImagePath1, ImagePath2, ImagePath3,
                            BottomOfPageImagePath, ScrollDownYPixels,
                            TakeScreenshot):
    try:
        x, y = pyautogui.locateCenterOnScreen(ImagePath1,
                                              grayscale=True,
                                              confidence=globalConfidence)
        ImagePath = ImagePath1
    except:
        print("Image @ Path 1 Not Found: " + str(ImagePath1))

    try:
        x, y = pyautogui.locateCenterOnScreen(ImagePath2,
                                              grayscale=True,
                                              confidence=globalConfidence)
        ImagePath = ImagePath2
    except:
        print("Image @ Path 2 Not Found: " + str(ImagePath2))

    try:
        x, y = pyautogui.locateCenterOnScreen(ImagePath3,
                                              grayscale=True,
                                              confidence=globalConfidence)
        ImagePath = ImagePath3
    except:
        print("Image @ Path 3 Not Found: " + str(ImagePath3))

    try:
        if (TakeScreenshot == TRUE):
            screenshot_x, screenshot_y = screenshotXYOffset(x, y)
            takeScreenshot(screenshot_x, screenshot_y)
        pyautogui.click(x, y)
        print("Clicked on image from path: " + str(ImagePath))
    except:
        print("Image was not found: " + str(ImagePath) + "\nScrolling down...")
        scroll(-int(ScrollDownYPixels))
        try:
            bottom_x, bottom_y = pyautogui.locateCenterOnScreen(
                BottomOfPageImagePath,
                grayscale=True,
                confidence=globalConfidence)
            if (bottom_x > 0 or bottom_y > 0):
                print(
                    "Image was not found & Bottom of page reached, skipping..."
                )
                return
        except:
            print("Bottom of page not reached, trying again...")
            clickMultiBaseLineImage(ImagePath1, ImagePath2, ImagePath3,
                                    BottomOfPageImagePath, ScrollDownYPixels,
                                    TakeScreenshot)


def clickFromLocation(ImagePath):
    try:
        x, y = pyautogui.locateCenterOnScreen(ImagePath,
                                              grayscale=True,
                                              confidence=globalConfidence)
        pyautogui.click(x, y)
        print("Clicked on image from path: " + str(ImagePath))
    except:
        print("Image was not found, skipping!")


def clickFromLocationReturnBool(ImagePath):
    try:
        x, y = pyautogui.locateCenterOnScreen(ImagePath,
                                              grayscale=True,
                                              confidence=globalConfidence)
        if x > 0:
            print("Found on image from path: " + str(ImagePath))
            return TRUE
    except:
        print("Image was not found, skipping!")


def clickFromLocationConfidence(ImagePath, Confidence):
    try:
        x, y = pyautogui.locateCenterOnScreen(ImagePath,
                                              grayscale=True,
                                              confidence=Confidence)
        pyautogui.click(x, y)
        print("Clicked on image from path: " + str(ImagePath))
    except:
        print("Image (" + str(ImagePath) + ") was not found, skipping!")


def clickImageMoveY(ImagePath, LeftOrRightPixels):
    try:
        x, y = pyautogui.locateCenterOnScreen(ImagePath,
                                              grayscale=True,
                                              confidence=globalConfidence)
        mod_x = x + int(LeftOrRightPixels)
        pyautogui.click(mod_x, y)
        print("Clicked on " + LeftOrRightPixels +
              " PIXELS on Y Axis away from image from path: " + str(ImagePath))
    except:
        print("Unable to find image")


def sequence():
    defaultLoc()
    clickMultiBaseLineImage(baselineCheckImg1, baselineCheckImg2,
                            baselineCheckImg3, baselineBottomOfPageImg, 108,
                            TRUE)
    wait(defaultWaitTimeSecs)
    clickBaseLineImage(editInvestmentImg, baselineBottomOfPageImg, 108, FALSE)
    wait(defaultWaitTimeSecs)
    clickImageMoveY(frequencyImg, 300)
    wait(defaultWaitTimeSecs)
    clickFromLocation(changeFrequencyImg)
    wait(defaultWaitTimeSecs)
    clickFromLocation(reviewChangesImg)
    wait(defaultWaitTimeSecs)
    clickFromLocation(saveChangesImg)
    wait(defaultWaitTimeSecs)
    clickFromLocationConfidence(getLatestScreenshot(), 0.95)
    wait(defaultWaitTimeSecs)


counter = 1
while (counter < 100):

    if clickFromLocationReturnBool(robinhoodImg) == TRUE:
        try:
            print("\nSequence #" + str(counter) + " started!")
            sequence()
            print("---------- Completed Sequence #" + str(counter) +
                  "----------\n")
            counter += 1
        except KeyboardInterrupt:
            print("Keyboard interrupt detected!")
            moveScreenshots()
        except:
            moveScreenshots()
    else:
        print("You are not on the robinhood page. Exiting!")
        counter = 100
