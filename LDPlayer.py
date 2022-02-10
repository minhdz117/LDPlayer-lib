import subprocess

PATH_LDP = '"' + "C:\LDPlayer\LDPlayer4.0\ldconsole.exe" + '"'


class LDPlayers ():
    def __init__(self, path: str = PATH_LDP) -> None:
        sp = subprocess.Popen(path, shell=True, stdout=subprocess.PIPE)
        if "dnplayer Command Line Management Interface" not in sp.stdout.readline().decode():
            raise SystemError("Ldconsole not found")
        self.path = path

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
                raise ValueError("Value not None")

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
