from email.mime import image
import subprocess
import os
import time
import cv2
import numpy as np
PATH_LDP = '"' + "C:\LDPlayer\LDPlayer4.0\ldconsole.exe" + '"'


class Keys():
    HOME = '3'
    BACK = '4'
    CALL = '5'
    END_CALL = '6'
    VOL_UP = '24'
    VOL_DOWN = '25'
    POWER = '26'
    CAMERA = '27'
    BROWSER = '64'
    ENTER = '66'
    BACKSPACE = '67'
    PHONEBOOK = '207'
    LIGHT_UP = '220'
    LIGHT_DOWN = '221'
    CUT = '277'
    COPY = '278'
    PATSE = '279'


class LDPlayers ():
    def __init__(self, path: str = PATH_LDP) -> None:
        sp = subprocess.Popen(path, shell=True, stdout=subprocess.PIPE)
        if "dnplayer Command Line Management Interface" not in sp.stdout.readline().decode():
            raise SystemError("Ldconsole not found")
        self.path = path
        subprocess.Popen(f"""{path} adb --index 0 --command "start-server" """)

    def find_by_index(self, index: int):
        sp = subprocess.Popen(self.path + " list",
                              shell=True, stdout=subprocess.PIPE)
        count = -1
        while sp.stdout.readline():
            count += 1
        if index > -1 and index <= count:
            return LDPlayer(path=self.path, index=index)
        else:
            raise ValueError("LDPlayer is not found")

    def find_by_name(self, name: str):
        sp = subprocess.Popen(self.path + " list",
                              shell=True, stdout=subprocess.PIPE)
        while line := sp.stdout.readline().decode().strip():
            if name == line:
                return LDPlayer(path=self.path, name=name)
        raise ValueError("LDPlayer is not found")

    def show(self):
        print(subprocess.Popen(self.path + " list", shell=True))

    def create(self, name: str):
        print(subprocess.Popen(self.path + " add --name " + name, shell=True))

    def delete_by_name(self, name: str):
        print(subprocess.Popen(self.path + " remove --name " + name, shell=True))

    def delete_by_index(self, index: int):
        print(subprocess.Popen(self.path + " remove --index " + index, shell=True))

    def copy(self, name: str, fromName: str):
        print(subprocess.Popen(self.path + " copy --name " +
              name + " --from " + fromName, shell=True))

    def quitall(self):
        print(subprocess.Popen(self.path + " quitall", shell=True))


class LDPlayer ():
    def __init__(self, path: str, index: int = None, name: str = None) -> None:
        if index != None:
            self.index = str(index)
            self.path = path
            self.name = None
        elif name:
            self.name = name
            self.path = path
            self.index = None

    def setup(self, resolution: list[int, int, int], cpu: int, memory: int, manufacturer: str, model: str, pnumber: str, imei: str, imsi: str, simserial: str, androidid: str, mac: str, autorotate: bool, lockwindow: bool) -> None:
        if self.index:
            cmd = " modify --index " + str(self.index)
        elif self.name:
            cmd = " modify --name " + self.name

        if resolution:
            cmd += " --resolution " + \
                resolution[0] + ',' + resolution[1] + ',' + resolution[2]

        if cpu:
            if (cpu > 0 and cpu < 5):
                cmd += " --cpu " + cpu
            else:
                raise ValueError("Value must be 1,2,3,4")

        if memory:
            if memory in [256, 512, 1024, 2048, 4096, 6144, 8192]:
                cmd += " --memory " + memory
            else:
                raise ValueError(
                    "Value must be 256, 512, 1024, 2048, 4096, 6144, 8192")

        if manufacturer:
            cmd += " --manufacturer " + manufacturer
            if model:
                cmd += " --model " + model
            else:
                raise ValueError("Model value is not None")

        if pnumber:
            cmd += " --pnumber " + pnumber

        if imei:
            cmd += " --imei " + imei
        else:
            cmd += " --imei auto"

        if imsi:
            cmd += " --imsi " + imsi

        if simserial:
            cmd += " --simserial " + simserial

        if androidid:
            cmd += " --androidid " + androidid

        if mac:
            cmd += " --mac " + mac

        if autorotate:
            cmd += " --autorotate " + int(autorotate)

        if lockwindow:
            cmd += " --lockwindow " + int(lockwindow)

        print(subprocess.Popen(self.path + cmd, shell=True))

    def run(self):
        if self.name:
            print(subprocess.Popen(self.path +
                  " launch --name " + self.name, shell=True))
        elif self.index:
            print(subprocess.Popen(self.path +
                  " launch --index " + self.index, shell=True))

    def quit(self):
        if self.name:
            print(subprocess.Popen(self.path +
                  " quit --name " + self.name, shell=True))
        elif self.index:
            print(subprocess.Popen(self.path +
                  " quit --index " + self.index, shell=True))

    def click(self, x: int, y: int):
        if self.name:
            print(subprocess.Popen(self.path + " adb --name " + '"' + self.name +
                  '"' + " --command " + '"' + "shell input tap " + x + " " + y + '"'))
        elif self.index:
            print(subprocess.Popen(self.path + " adb --index " + self.index +
                  " --command " + '"' + "shell input tap " + x + " " + y + '"'))

    def click_to_image(self, image: str):
        self.screen_cap()
        if self.name:
            pos = self.get_pos_click(os.path.abspath(
                f"images-screencap/{self.name}.png"), image)
            if pos:
                x, y = pos[0]
                print(subprocess.Popen(self.path + " adb --name " + '"' + self.name +
                                       '"' + " --command " + '"' + "shell input tap " + str(x) + " " + str(y) + '"'))

        elif self.index:
            pos = self.get_pos_click(os.path.abspath(
                f"images-screencap/index{self.index}.png"), image)
            if pos:
                x, y = pos[0]
                print(subprocess.Popen(self.path + " adb --index " + self.index +
                                       " --command " + '"' + "shell input tap " + str(x) + " " + str(y) + '"'))
    
    def wait_image(self, image:str, timeout:int = 10):
        if self.name:
            while not self.get_pos_click(os.path.abspath(
                f"images-screencap/{self.name}.png"), image) and timeout>0:
                time.sleep(0.5)
                timeout -=1
            if timeout<1 :
                raise TimeoutError("Can't find image on screen")
            else :
                return True

        elif self.index:
            while not self.get_pos_click(os.path.abspath(
                f"images-screencap/index{self.index}.png"), image) and timeout>0:
                time.sleep(0.5)
                timeout -=1
            if timeout<1 :
                raise TimeoutError("Can't find image on screen")
            else :
                return True

    def send_text(self, text: str):
        if self.name:
            print(subprocess.Popen(self.path + " adb --name " + '"' + self.name +
                  '"' + " --command " + '"' + "shell input text \'" + text + '\'"'))
        elif self.index:
            print(subprocess.Popen(self.path + " adb --index " + self.index +
                  " --command " + '"' + "shell input text \'" + text + '\'"'))

    def send_key_event(self, key: str):
        if self.name:
            print(subprocess.Popen(self.path + " adb --name " + '"' + self.name +
                  '"' + " --command " + '"' + "shell keyevent " + key + '"'))
        elif self.index:
            print(subprocess.Popen(self.path + " adb --index " + self.index +
                  " --command " + '"' + "shell keyevent " + key + '"'))

    def screen_cap(self):
        if self.name:
            os.makedirs(os.path.abspath("images-screencap"), exist_ok=True)
            print(subprocess.Popen(
                f"""{self.path} adb --name "{self.name}" --command "shell screencap -p /sdcard/{self.name}.png" """, shell=True))
            time.sleep(0.5)
            print(subprocess.Popen(
                f"""{self.path} adb --name "{self.name}" --command "pull /sdcard/{self.name}.png {os.path.abspath("images-screencap")}" """))
        elif self.index:
            os.makedirs(os.path.abspath("images-screencap"), exist_ok=True)
            print(subprocess.Popen(
                f"""{self.path} adb --index {self.index} --command "shell screencap -p /sdcard/index{self.index}.png" """, shell=True))
            time.sleep(0.5)
            print(subprocess.Popen(
                f"""{self.path} adb --index {self.index} --command "pull /sdcard/index{self.index}.png {os.path.abspath("images-screencap")}" """, shell=True))

    @classmethod
    def get_pos_click(
        cls,
        cap: str,
        obj: str,
        center: bool = True,
        multi: bool = False,
        threshold: float = 0.8,
        eps: float = 0.05,
        show: bool = False
    ) -> list:
        img_base = cv2.imread(cap)
        img_find = cv2.imread(obj)
        width = img_find.shape[1]
        height = img_find.shape[0]
        result = cv2.matchTemplate(img_base, img_find, cv2.TM_CCOEFF_NORMED)
        pos = []
        if multi:
            y_loc, x_loc = np.where(result >= threshold)
            rectangles = []
            for x, y in zip(x_loc, y_loc):
                rectangles.append([int(x), int(y), int(width), int(height)])
                rectangles.append([int(x), int(y), int(width), int(height)])
            for x, y, w, h in cv2.groupRectangles(rectangles, 1, eps)[0]:
                cv2.rectangle(img_base, (x, y), (x + w, y + h), (0, 0, 255), 2)
                if center:
                    pos.append((x + w // 2, y + h // 2))
                else:
                    pos.append((x, y))
        else:
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            if max_val > threshold:
                cv2.rectangle(
                    img_base, max_loc, (max_loc[0] + width, max_loc[1] + height), (0, 0, 255), 2)
                if center:
                    pos.append((max_loc[0] + width // 2,
                               max_loc[1] + height // 2))
                else:
                    pos.append(max_loc)
        if show:
            cv2.imshow("show", img_base)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return pos
