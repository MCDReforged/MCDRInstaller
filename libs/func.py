import ctypes
import hashlib
import os
import re
import subprocess
import tempfile
import time

import requests
import wx
from lxml import etree
from pefile import PE
from ui.main import LinkDialog

# logger = logging.getLogger('mcdr_installer')
# logger.setLevel(logging.DEBUG)
# logging.basicConfig(filename='log.log', level=logging.DEBUG)

def get_all_python():
    data = requests.get('https://www.python.org/downloads/windows/').text
    page = etree.HTML(data)
    key_list = ['x86-64 executable installer', 'installer (64-bit)']
    version_list = {}
    for ver in page.xpath("//div[@class='column'][1]/ul/li"):
        if ver.find('ul/li').text.startswith('No files for this release.'):
            continue
        for file in ver.findall('ul/li/a'):
            for key in key_list:
                if key in file.text.lower():
                    link = file.get('href')
                    version = re.search('([1-9]\d|[1-9])(\.([1-9]\d|\d)){2}', ver.find('a').text)
                    if version is not None:
                        version_list[version.group(0)] = link
    return version_list

def verify_sha256(file, cert):
    with open(file, 'rb') as f:
        data = f.read()
    hash = hashlib.sha256()
    hash.update(data)
    if hash.hexdigest() == cert:
        return True
    return False

def have_cert(file) -> bool:
    pe = PE(file)
    IMAGE_DIRECTORY_ENTRY_SECURITY = str(pe.OPTIONAL_HEADER.DATA_DIRECTORY[4])
    pattern1 = r'VirtualAddress:\s+0x0\b'
    pattern2 = r'Size:\s+0x0\b'
    if pattern1 not in IMAGE_DIRECTORY_ENTRY_SECURITY and pattern2 not in IMAGE_DIRECTORY_ENTRY_SECURITY:
        return True

def run_command(cmd: str) -> str:
    """A popen func For pyinstaller -w"""
    def decode_utf8_fix(b):
        try:
            return b.decode('utf8').replace('\r\n', '\n')
        except UnicodeDecodeError:
            return ''
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    process = subprocess.Popen(cmd, startupinfo=startupinfo, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    while process.poll() is None:
        time.sleep(0.1)
    return (process.returncode, decode_utf8_fix(process.stdout.read()))


def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def have_chinese(text):
    for c in text:
        """????????????unicode???????????????"""
        if c >= u'\u4e00' and c <= u'\u9fa5':
            return True
    return False

def choose_folder(parent) -> str:
    dlg = wx.DirDialog(parent, '???????????????')
    if dlg.ShowModal() == wx.ID_OK:
        path = dlg.GetPath()
        if os.listdir(path):
            message_box(parent, '??????', '????????????????????????????????????...', wx.ICON_WARNING)
            return choose_folder(parent)
        if have_chinese(path):
            message_box(parent, '??????', '????????????????????????????????????...', wx.ICON_WARNING)
            return choose_folder(parent)
        return path
    dlg.Destroy()
    return ''


def message_box(parent, title, message, icon_type) -> None:
    dlg = wx.MessageDialog(parent, message, title, wx.OK | icon_type)
    dlg.ShowModal()
    dlg.Destroy()

def ask_box(parent, title, message) -> bool:
    dlg = LinkDialog(parent, title,  message)
    if dlg.ShowModal() == wx.ID_YES:
        return True
    return False


def download_file(filename, url, progressbar: wx.Gauge) -> bool:
    """???????????????

    Args:
        filename (str): ???????????????
        url (str): ?????? URL
        progressbar (wx.Gauge): ???????????????

    Returns:
        bool: ??????????????????
    """
    try:
        headers = {'Proxy-Connection':'keep-alive'}
        r = requests.get(url, stream=True, headers=headers)
        f = open(filename, 'wb')
        length = float(r.headers['content-length'])
        count = last_count = 0
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                count += len(chunk)
                progress = count / length * 100
                speed = (count-last_count) / 1048576 / 0.5
                last_count = count
                progressbar.SetValue(int(progress))
        f.close()
        return True
    except:
        f.close()
        os.remove(filename)
        return False

def temp(*paths: str) -> str:
    root = os.path.join(tempfile.gettempdir(), 'MCDRInstaller')
    if not os.path.isdir(root):
        os.mkdir(root)
    return os.path.join(root, *paths)

def create_url_file(name, url):
    with open(name + '.url', 'w') as f:
        f.write('[InternetShortcut]\nURL=' + url)

def create_mcdr_scripts(name1, name2):
    with open(name1 + '.bat', 'w') as f:
        f.write('@echo off\npython -m mcdreforged\npause')
    with open(name2 + '.bat', 'w') as f:
        f.write('@echo off\npip install mcdreforged --upgrade\npause')

def create_minecraft_eula():
    with open('eula.txt', 'w') as f:
        f.write('#Generated by MCDRInstaller\neula=true')

if __name__ == '__main__':
    print(run_command('pip install mcdreforged --upgrade'))
