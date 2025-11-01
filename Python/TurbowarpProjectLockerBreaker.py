import json
import os
import re
import tempfile
import zipfile

class TurbowarpProjectLockerBreaker:
    def __init__(self, project_path):
        self.project_path = project_path
        if not os.environ.get("temp_dir"):
            self.temp_dir = tempfile.gettempdir()
        else:
            self.temp_dir = os.environ["temp_dir"]
        self.temp_dir = os.path.join(self.temp_dir, "TurbowarpProjectLockerBreaker")

    def unzip(self):
        zip_file = zipfile.ZipFile(self.project_path)
        zip_file.extractall(self.temp_dir)
        zip_file.close()

    def parse_json(self):
        with open(os.path.join(self.temp_dir, "project.json"), encoding="utf-8") as f:
            data = f.read()
            data = re.sub(r"\\\"", "'", data)
            data = json.loads(data)
            return data

    @staticmethod
    def custom_decrypt(encrypted_text, key):
        try:
            encrypted_array = encrypted_text.split('-')
            decrypted = []
            key_length = len(key)
            for i in range(len(encrypted_array)):
                encrypted_char = int(encrypted_array[i], 16)
                encrypted_char ^= 0x55
                encrypted_char = encrypted_char // (i + 1)  # 使用整数除法
                encrypted_char -= key_length
                key_code = ord(key[i % key_length])
                original_char = encrypted_char ^ key_code
                decrypted.append(chr(original_char))
            return str().join(decrypted)
        except Exception as e:
            print(f"解密错误: {e}")
            return None

    def removeProjectLocker(self):
        pass

    def get_password(self, data):
        variables:dict = data.get("targets")[0].get("variables")
        decrypt_info_index = ""
        for index, variable in variables.items():
            if variable[0] == "_passwordSettings":
                decrypt_info_index = index
        if decrypt_info_index == "":
            return False, "未找到加密信息"
        decrypt_info_json = variables[decrypt_info_index][1]
        decrypt_info_json = re.sub(r"\'", "\"", decrypt_info_json)
        decrypt_info = json.loads(decrypt_info_json)
        encrypted_password = decrypt_info.get("encryptedPassword")
        encryption_key = decrypt_info.get("encryptionKey")
        password = self.custom_decrypt(encrypted_password, encryption_key)
        return True, password, encrypted_password, encryption_key


    def autorun(self):
        print(f"正在解压缩文件 {self.project_path} 到 {self.temp_dir}")
        self.unzip()
        print("正在解析project.json")
        data = self.parse_json()
        print("正在解密密码")
        result = self.get_password(data)
        if result[0]:
            print(f"密码为：{result[1]}")
            print(f"加密后的数据为：{result[2]}")
            print(f"加密密钥为：{result[3]}")
        else:
            print(result[1:])
        print("删除项目锁的代码正在编写，敬请期待")


def main():
    project_path = input("请输入项目文件路径(.sb3文件位置)：")
    if not os.path.exists(project_path) or not os.path.isfile(project_path):
        print("这不是一个项目文件")
    else:
        TurbowarpProjectLockerBreaker(project_path).autorun()

if __name__ == '__main__':
    main()