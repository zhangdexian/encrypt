import sys
import os
from Crypto.Cipher import AES
import base64


def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)


KEY = add_to_16("zdx520")
SEP = "火影忍者".encode('utf-8')


class EncryptUtil():

    def __init__(self, cwd, exclude):
        self.cwd = cwd
        self.exclude = exclude
        self.dir_name = os.path.basename(os.path.abspath(self.cwd))
        self.origin_cwd = os.path.abspath(os.path.curdir)
        self.target = f'{os.path.join(self.origin_cwd, "generator")}.zip'

    def zip(self):
        command = f'zip -rvq {self.target} "."'
        if self.exclude is not None:
            excludeList = self.exclude.split(",")
            for i in excludeList:
                command += f' -x "{i}"'
        print(f'正在执行:{command}')
        os.system(command)

    def add_data(self):

        content = ''

        with open("./generator.zip", "rb") as f:
            content = f.read()

        aes = AES.new(KEY, AES.MODE_ECB)
        content = str(base64.encodebytes(content), "utf-8")
        content = add_to_16(content)
        encrypt_content = aes.encrypt(content)

        with open("./night.jpeg", "rb") as f:
            with open("./generator.jpeg", "wb+") as w:
                w.write(f.read())
                w.write(SEP)
                w.write(encrypt_content)

    def encrypt(self):
        os.chdir(self.cwd)
        self.zip()
        os.chdir(self.origin_cwd)
        self.add_data()

    def decrypt(self):
        content = ''
        with open("./generator.jpeg", "rb") as f:
            content = f.read()
            index = content.find(SEP)
            content = content[index + len(SEP):]
        aes = AES.new(KEY, AES.MODE_ECB)
        content = aes.decrypt(content)
        content = str(content, "utf-8").replace('\0', '')
        content = base64.decodebytes(bytes(content, "utf-8"))

        with open('./result.zip', 'wb+') as f:
            f.write(content)


def main():
    command = sys.argv[1]
    cwd = '.'
    exclude = ''
    if len(sys.argv) >= 3:
        cwd = sys.argv[2]
        exclude = sys.argv[3]

    encryptUtil = EncryptUtil(cwd, exclude)
    if command != "1":
        encryptUtil.decrypt()
        return
    encryptUtil.encrypt()


main()
