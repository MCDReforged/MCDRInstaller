import os
import re
import shutil
import sys
import webbrowser
import winreg

import requests
import ruamel.yaml as yaml
import wx

from libs.func import *
from libs.new_thread import new_thread
from libs.semver import Version, VersionParsingError, VersionRequirement
from libs.settings import *
from ui.main import InstallFrame, SetFrame


class InstalltionError(Exception):
    pass


class InstallUI(InstallFrame):
    def __init__(self, parent, target):
        super().__init__(parent)
        self.target = target
        self.finished_task = 0
        self.task_count = len([i for i in self.target if self.target[i]])
        print(self.task_count)
        self.execute_install()

    def refresh_progress(self):
        self.finished_task += 1
        self.progress.SetValue(int(self.finished_task / self.task_count * 100))

    @new_thread
    def execute_install(self):
        try:
            if self.target['java']:
                self.install_java()
            if self.target['python']:
                self.install_python()
            if self.target['mcdr']:
                self.install_mcdr()
            self.configure_mcdr()
            if self.target['fabric']:
                self.install_fabric()
            message_box(self, '提示', '执行完成！\n享受你的 MCDR 之旅！', wx.ICON_INFORMATION)
        except Exception as e:
            message_box(self, '错误', '执行时发现错误。\n错误详情：' + str(e), wx.ICON_ERROR)
            raise
        finally:
            shutil.rmtree(temp())
            self.Close()

    def install_java(self):
        self.progress_text.SetLabel('安装 Java')

        self.subprogress_text.SetLabel('查找 AdoptOpenJRE 下载地址')
        self.progress.SetValue(0)
        filename = temp('java_installer.msi')
        link = JAVA_LINK.format(self.target['java'])
        data = requests.get(link).json()
        for i in data:
            if not i['prerelease'] and not 'openj9' in i['name']:
                release = i
                release_name = i['name'].replace('jdk', '').strip()
        for i in release['assets']:
            if i['name'].endswith('.msi') and 'jre' in i['name'] and 'x64' in i['name']:  # TODO: 优化检测
                download_link = i['browser_download_url']  # https://github.com/.../<name>.msi
                hash_link = download_link + '.sha256.txt'  # https://github.com/.../<name>.msi.sha256.txt

        self.subprogress_text.SetLabel('下载 AdoptOpenJRE' + release_name)
        if not download_file(filename, download_link, self.subprogress):
            raise InstalltionError('下载 JRE 安装文件失败。')
        cert = requests.get(hash_link).text
        cert = cert.splitlines()[0].split(' ')[0]  # Format: "<sha256> <filename>\n"

        self.subprogress_text.SetLabel('验证已下载文件')
        self.subprogress.SetValue(0)
        if not verify_sha256(filename, cert):
            raise InstalltionError('JRE 安装文件损坏。')
        self.subprogress.SetValue(100)

        self.msi_install(filename)

    def msi_install(self, filename):
        self.subprogress_text.SetLabel('安装 AdoptOpenJRE')
        self.subprogress.SetValue(0)
        if run_command(['msiexec', '/i', filename, 'INSTALLLEVEL=1', '/passive'])[0]:
            raise InstalltionError('安装 JRE 时发生错误。')
        self.subprogress.SetValue(100)

        self.refresh_progress()

    def install_python(self):
        self.subprogress.SetValue(0)
        self.progress_text.SetLabel('安装 Python')
        self.subprogress_text.SetLabel('下载 Python ' + self.target['python'])
        filename = temp('python_installer.exe')
        if not download_file(filename, PYTHON_LINK.format(self.target['python']), self.subprogress):
            raise InstalltionError('下载 Python 安装文件失败。')

        self.subprogress.SetValue(0)
        if not have_cert(filename):
            raise InstalltionError('Python 安装文件损坏。')
        self.subprogress.SetValue(100)

        self.subprogress.SetValue(0)
        self.subprogress_text.SetLabel('安装 Python ' + self.target['python'])
        if run_command([filename, '/passive', '/InstallAllUsers=1', '/CompileAll=1', '/PrependPath=1'])[0]:
            raise InstalltionError('安装 Python 时发生错误。')
        self.subprogress.SetValue(80)
        self.subprogress_text.SetLabel('解除 MAX_PATH 限制')
        try:
            winreg.SetValue(winreg.HKEY_LOCAL_MACHINE,
                            "SYSTEM\\CurrentControlSet\\Control\\FileSystem\\LongPathsEnabled", winreg.REG_DWORD, '1')
        except Exception:
            message_box(self, '警告', '解除 MAX_PATH 失败。\n这理论上不会有太大影响，让我们继续...', wx.ICON_WARNING)
        self.subprogress.SetValue(100)

        self.refresh_progress()

    def install_mcdr(self):
        self.subprogress.SetValue(0)
        self.progress_text.SetLabel('安装 MCDReforged')
        self.subprogress_text.SetLabel('配置 pip')
        run_command('python -m pip config set global.index-url ' + PIP_MIRROR)
        self.subprogress.SetValue(20)
        self.subprogress_text.SetLabel('使用 pip 安装 MCDReforged')
        if run_command('python -m pip install mcdreforged --upgrade')[0]:
            raise InstalltionError('安装 MCDR 时发生错误。')
        self.subprogress.SetValue(100)

        self.refresh_progress()

    def configure_mcdr(self):
        self.subprogress.SetValue(0)
        self.progress_text.SetLabel('部署 MCDReforged')
        os.chdir(self.target['path'])

        self.subprogress_text.SetLabel('执行 python 指令以部署 MCDReforged')
        if run_command('python -m mcdreforged', cwd='D:\\Temp\\新建文件夹')[0]:
            raise InstalltionError('部署 MCDR 时发生错误。')
        self.subprogress.SetValue(80)

        self.subprogress_text.SetLabel('修改 MCDReforged 配置文件')
        try:
            with open(os.path.join('config.yml'), 'r+', encoding='utf8') as f:
                data = yaml.safe_load(f)
                data['language'] = 'zh_cn'
                data['start_command'] = 'java -Xms1G -Xmx2G -jar fabric-server-launch.jar nogui'
                yaml.safe_dump(data, f)
        except Exception as e:
            raise InstalltionError('配置 MCDR 时发生错误：' + e)
        self.subprogress.SetValue(100)

        self.refresh_progress()

    def install_fabric(self):
        def get_fabric_link():
            for i in requests.get(FABRIC_CHECK_LINK.format('installer')).json():
                if i['stable']:
                    return i['url']
        os.chdir(os.path.join(self.target['path'], 'server'))
        self.subprogress.SetValue(0)
        self.progress_text.SetLabel('安装 Fabric')
        self.subprogress_text.SetLabel('下载 Fabric Installer')
        filename = temp('fabric_installer.jar')
        if not download_file(filename, get_fabric_link(), self.subprogress):
            raise InstalltionError('下载 Fabric Installer 失败。')

        self.subprogress.SetValue(0)
        self.subprogress_text.SetLabel(f"安装 Fabric Server (for Minecraft {self.target['fabric']})")
        if run_command(['java', '-jar', filename, 'server', '-mcversion', self.target['fabric'], '-downloadMinecraft'])[0]:
            raise InstalltionError('安装 Fabric 时发生错误。')
        self.subprogress.SetValue(100)

        self.refresh_progress()


class SetUI(SetFrame):
    env = {'python': None, 'java': None, 'mcdr': None}
    mcdr_requirement = VersionRequirement('>=3.6.0')

    def __init__(self, parent=None):
        super().__init__(parent)
        # if not is_admin(): # TODO
        #     message_box(self, '错误', '请以管理员身份运行，否则无法进行安装操作！', wx.ICON_ERROR)
        #     self.Close()
        #     return
        if not ask_box(self, '在开始之前，你需要明白一些事...', LICENSE_TEXT):
            self.Close()
            return
        self.check_env()
        self.load_versions()
        self.path_btn.Bind(wx.EVT_BUTTON, self.set_path)
        self.cancel_btn.Bind(wx.EVT_BUTTON, exit_app)
        self.fabric_box.Bind(wx.EVT_CHOICE, self.auto_select)
        self.execute_btn.Bind(wx.EVT_BUTTON, self.go_next)
        for i in ['java', 'python', 'fabric']:
            eval(f'self.{i}_check.Bind(wx.EVT_CHECKBOX, self.auto_select)')

    @new_thread
    def auto_select(self, event=None):
        minecraft_version = Version(self.fabric_box.GetStringSelection())
        if minecraft_version >= Version('1.17'):  # Minecraft 版本 -> 自动对应 Java 版本
            self.java_box.Select(2)
        elif minecraft_version >= Version('1.13'):
            self.java_box.Select(1)
        else:
            self.java_box.Select(0)
        for i in ['java', 'python', 'fabric']:  # 禁用未勾选项对应的选择框
            eval('self.{0}_box.Enable() if self.{0}_check.IsChecked() else self.{0}_box.Disable()'.format(i))
        if self.fabric_check.IsChecked() and not self.env['java']:  # 装 Fabric -> 必须有 Java
            self.java_check.SetValue(True)
            self.java_check.Disable()
        else:
            self.java_check.Enable()

    @new_thread
    def load_versions(self):
        def get_python_versions():
            last_version = VersionRequirement('~0.0.0')
            support = []
            version_list = [i['ref'].split('/')[-1].replace('v', '') for i in requests.get(PYTHON_CHECK_LINK).json()]
            version_list = [i for i in version_list if re.match('^[0-9.]*$', i)]
            version_list.sort(reverse=False)
            print(version_list)
            for version in version_list:
                try:
                    if self.mcdr_requirement.accept(version):
                        if version == version_list[-1]:
                            support.append(version)
                        elif not last_version.accept(version):
                            support.append(str(last_version)[1:])
                    last_version = VersionRequirement('~' + version)
                except VersionParsingError:
                    continue
            return support
        try:
            self.Disable()
            self.status_bar.SetStatusText(u'加载 Python 版本...')
            PYTHON_CHECK_List = get_python_versions()
            self.python_box.AppendItems(list(PYTHON_CHECK_List))
            self.python_box.Select(self.python_box.GetCount() - 1)
            self.status_bar.SetStatusText(u'加载 Minecraft 版本...')
            minecraft_versions = requests.get(FABRIC_CHECK_LINK.format('game')).json()
            fabric_versions = [i['version'] for i in minecraft_versions if i['stable']]
            self.fabric_box.AppendItems(fabric_versions)
            self.fabric_box.Select(0)
        except Exception as e:
            message_box(self, '错误', f'获取版本列表失败。如非网络错误，请将此错误提交 Issue。\n错误详情：{e}', wx.ICON_ERROR)
            self.status_bar.SetStatusText(u'错误。')
        else:
            self.Enable()
            self.auto_select()
            self.status_bar.SetStatusText(u'就绪。')

    def check_env(self):
        def extract_testfile():
            file = temp('test_mcdr.py')
            with open(file, 'w', encoding='utf8') as f:
                f.write(TEST_SCRIPT)
            return file
        self.status_bar.SetStatusText(u'检查系统环境...')
        java = python = mcdr = None
        # 检测 Java 是否安装
        cmd = run_command('java --version')
        if not cmd[0]:
            java = cmd[1].split('\n')[0]
            self.java_check.SetValue(False)
            self.java_text.SetLabel('已安装: ' + str(java))
            self.java_text.Show()
            self.env['java'] = java
        # 检测 Python 是否安装
        cmd = run_command('python --version')
        if not cmd[0]:
            python = Version(cmd[1].lower().replace('python', '').strip())
            self.python_check.SetValue(False)
            self.python_text.SetLabel('已安装: ' + str(python))
            self.env['python'] = python
            # 检测 MCDR 是否安装
            cmd = run_command('python ' + extract_testfile())
            if not cmd[0]:
                mcdr = Version(cmd[1])
                self.mcdr_check.SetValue(False)
                self.mcdr_text.SetLabel('已安装: ' + str(mcdr))
                self.env['mcdr'] = mcdr
        else:
            self.python_check.SetValue(True)
            self.python_check.Disable()

        # 获取 MCDR 兼容的 Python 版本
        data = requests.get(MCDR_CHECK_LINK).json()['info']
        requirement = VersionRequirement(data['requires_python'])
        self.mcdr_requirement = requirement
        # 检测已安装 Python 兼容性
        if self.env['python']:
            latest_mcdr = Version(data['version'])
            # self.env['python'] = Version('0.0.0')
            # self.env['mcdr'] = Version('0.0.0')
            if not requirement.accept(self.env['python']):
                self.python_text.SetLabel(f"不兼容最新 MCDR (已安装 {self.env['python']}, 需要 {requirement})")
                self.python_text.SetForegroundColour(YELLOW)
                message_box(
                    self, '错误',
                    f"当前 Python 与 MCDR 不兼容。 (已安装 {self.env['python']}, 需要 {requirement})\n请更新 Python。",
                    wx.ICON_WARNING)
                webbrowser.open(PYTHONUPDATER_LINK)
                exit_app()
                return
            # 检测 MCDR 是否最新
            if self.env['mcdr'] and latest_mcdr > self.env['mcdr']:
                self.mcdr_check.SetLabel('更新 MCDReforged')
                self.mcdr_check.SetValue(True)
                self.mcdr_text.SetLabel(f"不是最新 (已安装 {self.env['mcdr']}, 最新 {latest_mcdr})")
                self.mcdr_text.SetForegroundColour(YELLOW)

    def set_path(self, *args):
        self.path_text.SetValue(choose_folder(self))

    def go_next(self, *args):
        if not self.path_text.GetValue():
            message_box(self, '错误', '未填写安装路径', wx.ICON_ERROR)
            return
        target = {
            'path': self.path_text.GetValue(),
            'java': self.java_box.GetStringSelection() if self.java_check.IsChecked() else None,
            'python': self.python_box.GetStringSelection() if self.python_check.IsChecked() else None,
            'mcdr': self.mcdr_check.IsChecked(),
            'fabric': self.fabric_box.GetStringSelection() if self.fabric_check.IsChecked() else None
        }
        execute(target)

def exit_app(*args):
    try:
        app.ExitMainLoop()
        sys.exit()
    except:
        pass

def execute(target):
    main_win.Close()
    install_win = InstallUI(None, target)
    install_win.Show()


if __name__ == '__main__':
   # 下面是使用wxPython的固定用法
    app = wx.App()
    main_win = SetUI(None)
    # main_win = LicenseUI(None)
    main_win.Show()
    sys.exit(app.MainLoop())
