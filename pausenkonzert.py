import pyautogui
import pyperclip
import time
import datetime
import json


def button_check(img, click, t=0):

    try:
        buttonx, buttony = pyautogui.locateCenterOnScreen(img, grayscale=True)
        print ("Found Button " + img)

        if click:
            pyautogui.click(buttonx, buttony) 
            time.sleep(t)
            pyautogui.click(1, 1) 
        return True
    except TypeError:
        return False


def inc_votes ():
    with open('votes.json', 'r') as f:
        data = json.load(f)

    data["votes"] += 1
    data["last_vote"] = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())

    with open('votes.json', 'w') as json_file:
        json.dump(data, json_file)

    return data["votes"]


if __name__ == '__main__':

    pyautogui.FAILSAFE = False
  
    while True:

        found = False

        hour = int(time.strftime("%H", time.localtime()))
        if hour < 5 or hour > 21:
            print ("Night Break")
            time.sleep(60)
            continue

        found |= button_check('./img/jetzt_abstimmen.png', True, 3)
        found |= button_check('./img/jetzt_abstimmen2.png', True, 3)

        found |= button_check('./img/antirobot.png', True, 10)

        if button_check('./img/stimme_abgeben.png', True, 60):
            if button_check('./img/geklappt.png', False):
                print ("Votes=" + str(inc_votes()))
                found = True

        # start url if lost
        if not found:
            try:
                print("Resover url")
                buttonx, buttony = pyautogui.locateCenterOnScreen("./img/ctrl.png", grayscale=True)
                pyautogui.click(buttonx+300, buttony) 
                time.sleep(1)

                url = 'www.antenne.de/programm/aktionen/pausenhofkonzerte/schulen/10316-maria-ward-schule-mdchengymnasium-der-maria-ward-stiftung-aschaffenburg'
                for c in url:
                    if c == "/":
                        pyautogui.hotkey('shift', '7', interval = 0.15)
                    else:
                        pyautogui.write(c)
                pyautogui.press('enter')
            except TypeError:
                pass
            
                                                                    
        time.sleep(2)
