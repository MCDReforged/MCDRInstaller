from wx import Colour
import tempfile
import os

LICENSE_TEXT = '''
使用 MCDR Installer ，意味着你同意：
https://github.com/MCDReforged/MCDRInstaller/blob/master/LICENSE

安装 Python，意味着你同意：
https://docs.python.org/zh-cn/3/license.html#psf-license

安装 Minecraft Server 和 Fabric Loader，意味着你同意：
https://account.mojang.com/documents/minecraft_eula (Minecraft Server)
https://github.com/FabricMC/fabric-installer/blob/master/LICENSE (FabricMC)

安装 AdoptOpenJRE，意味着你同意：
https://github.com/AdoptOpenJDK/openjdk-jdk11u/blob/master/LICENSE
'''.strip()

GREEN = Colour(51, 153, 51)
YELLOW = Colour(255, 102, 0)

TEMP = os.path.join(tempfile.gettempdir(), 'MCDRInstaller')
TEST_SCRIPT = '''
try:
    from mcdreforged.constants.core_constant import VERSION,GITHUB_API_LATEST
except:
    from mcdreforged.constant import VERSION,GITHUB_API_LATEST
print(VERSION, end='')
'''.rstrip()

def GITHUB_DOWN_MIRROR(link):
    return link.replace('//github.com', '//download.fastgit.org')

PIP_MIRROR = 'https://mirrors.aliyun.com/pypi/simple/'

JAVA_LINK = 'https://api.github.com/repos/AdoptOpenJDK/openjdk{}-binaries/releases'

# PYTHON_LINK = 'https://www.python.org/ftp/python/{0}/python-{0}-amd64.exe'
# PYTHON_CHECK_LINK = 'https://api.github.com/repos/python/cpython/git/refs/tags'
# PYTHON_BLACKLIST = ['3.8.11', ]

# FABRIC_LINK = 'https://maven.fabricmc.net/net/fabricmc/fabric-installer/{0}/fabric-installer-{0}.jar'
FABRIC_LINK = 'https://download.mcbbs.net/maven/net/fabricmc/fabric-installer/{0}/fabric-installer-{0}.jar' 

MCDR_CHECK_LINK = 'https://pypi.org/pypi/mcdreforged/json'
PYTHONUPDATER_LINK = 'https://github.com/eagle3236/PythonUpdater'
# FABRIC_CHECK_LINK = 'https://meta.fabricmc.net/v2/versions/{}'
FABRIC_CHECK_LINK = 'https://download.mcbbs.net/fabric-meta/v2/versions/{}'

MCDR_PLG_URL = 'https://github.com/MCDReforged/PluginCatalogue/blob/master/readme_cn.md'