#!/usr/bin/python
import sys, argparse, urllib2
from os import listdir
from os.path import isfile, isdir, join, lexists

def log_err(*kwargs):
    msg = ''
    for item in kwargs:
        msg += str(item) + ' '

    sys.stderr.write(msg + '\n')


class DependencyExtracter(object):
    def __init__(self, version='2.7'):
        super(DependencyExtracter, self).__init__()
        self.version = version
        self.builtin_modules = ['\\', '__builtin__', '__future__', '__main__', '_winreg', 'abc', 'aepack', 'aetools', 'aetypes', 'aifc', 'al', 'AL', 'anydbm', 'applesingle', 'argparse', 'array', 'ast', 'asynchat', 'asyncore', 'atexit', 'audioop', 'autoGIL', 'base64', 'BaseHTTPServer', 'Bastion', 'bdb', 'binascii', 'binhex', 'bisect', 'bsddb', 'buildtools', 'bz2', 'calendar', 'Carbon', 'Carbon.AE', 'Carbon.AH', 'Carbon.App', 'Carbon.Appearance', 'Carbon.CarbonEvents', 'Carbon.CarbonEvt', 'Carbon.CF', 'Carbon.CG', 'Carbon.Cm', 'Carbon.Components', 'Carbon.ControlAccessor', 'Carbon.Controls', 'Carbon.CoreFounation', 'Carbon.CoreGraphics', 'Carbon.Ctl', 'Carbon.Dialogs', 'Carbon.Dlg', 'Carbon.Drag', 'Carbon.Dragconst', 'Carbon.Events', 'Carbon.Evt', 'Carbon.File', 'Carbon.Files', 'Carbon.Fm', 'Carbon.Folder', 'Carbon.Folders', 'Carbon.Fonts', 'Carbon.Help', 'Carbon.IBCarbon', 'Carbon.IBCarbonRuntime', 'Carbon.Icns', 'Carbon.Icons', 'Carbon.Launch', 'Carbon.LaunchServices', 'Carbon.List', 'Carbon.Lists', 'Carbon.MacHelp', 'Carbon.MediaDescr', 'Carbon.Menu', 'Carbon.Menus', 'Carbon.Mlte', 'Carbon.OSA', 'Carbon.OSAconst', 'Carbon.Qd', 'Carbon.Qdoffs', 'Carbon.QDOffscreen', 'Carbon.Qt', 'Carbon.QuickDraw', 'Carbon.QuickTime', 'Carbon.Res', 'Carbon.Resources', 'Carbon.Scrap', 'Carbon.Snd', 'Carbon.Sound', 'Carbon.TE', 'Carbon.TextEdit', 'Carbon.Win', 'Carbon.Windows', 'cd', 'cfmfile', 'cgi', 'CGIHTTPServer', 'cgitb', 'chunk', 'cmath', 'cmd', 'code', 'codecs', 'codeop', 'collections', 'ColorPicker', 'colorsys', 'commands', 'compileall', 'compiler', 'compiler.ast', 'compiler.visitor', 'ConfigParser', 'contextlib', 'Cookie', 'cookielib', 'copy', 'copy_reg', 'cPickle', 'cProfile', 'crypt', 'cStringIO', 'csv', 'ctypes', 'curses', 'curses.ascii', 'curses.panel', 'curses.textpad', 'datetime', 'dbhash', 'dbm', 'decimal', 'DEVICE', 'difflib', 'dircache', 'dis', 'distutils', 'distutils.archive_util', 'distutils.bcppcompiler', 'distutils.ccompiler', 'distutils.cmd', 'distutils.command', 'distutils.command.bdist', 'distutils.command.bdist_dumb', 'distutils.command.bdist_msi', 'distutils.command.bdist_packager', 'distutils.command.bdist_rpm', 'distutils.command.bdist_wininst', 'distutils.command.build', 'distutils.command.build_clib', 'distutils.command.build_ext', 'distutils.command.build_py', 'distutils.command.build_scripts', 'distutils.command.check', 'distutils.command.clean', 'distutils.command.config', 'distutils.command.install', 'distutils.command.install_data', 'distutils.command.install_headers', 'distutils.command.install_lib', 'distutils.command.install_scripts', 'distutils.command.register', 'distutils.command.sdist', 'distutils.core', 'distutils.cygwinccompiler', 'distutils.debug', 'distutils.dep_util', 'distutils.dir_util', 'distutils.dist', 'distutils.emxccompiler', 'distutils.errors', 'distutils.extension', 'distutils.fancy_getopt', 'distutils.file_util', 'distutils.filelist', 'distutils.log', 'distutils.msvccompiler', 'distutils.spawn', 'distutils.sysconfig', 'distutils.text_file', 'distutils.unixccompiler', 'distutils.util', 'distutils.version', 'dl', 'doctest', 'DocXMLRPCServer', 'dumbdbm', 'dummy_thread', 'dummy_threading', 'EasyDialogs', 'email', 'email.charset', 'email.encoders', 'email.errors', 'email.generator', 'email.header', 'email.iterators', 'email.message', 'email.mime', 'email.parser', 'email.utils', 'encodings', 'encodings.idna', 'encodings.utf_8_sig', 'errno', 'exceptions', 'fcntl', 'filecmp', 'fileinput', 'findertools', 'FL', 'fl', 'flp', 'fm', 'fnmatch', 'formatter', 'fpectl', 'fpformat', 'fractions', 'FrameWork', 'ftplib', 'functools', 'future_builtins', 'gc', 'gdbm', 'gensuitemodule', 'getopt', 'getpass', 'gettext', 'gl', 'GL', 'glob', 'grp', 'gzip', 'hashlib', 'heapq', 'hmac', 'hotshot', 'hotshot.stats', 'htmlentitydefs', 'htmllib', 'HTMLParser', 'httplib', 'ic', 'icopen', 'imageop', 'imaplib', 'imgfile', 'imghdr', 'imp', 'importlib', 'imputil', 'inspect', 'io', 'itertools', 'jpeg', 'json', 'keyword', 'lib2to3', 'linecache', 'locale', 'logging', 'logging.config', 'logging.handlers', 'macerrors', 'MacOS', 'macostools', 'macpath', 'macresource', 'mailbox', 'mailcap', 'marshal', 'math', 'md5', 'mhlib', 'mimetools', 'mimetypes', 'MimeWriter', 'mimify', 'MiniAEFrame', 'mmap', 'modulefinder', 'msilib', 'msvcrt', 'multifile', 'multiprocessing', 'multiprocessing.connection', 'multiprocessing.dummy', 'multiprocessing.managers', 'multiprocessing.pool', 'multiprocessing.sharedctypes', 'mutex', 'Nav', 'netrc', 'new', 'nis', 'nntplib', 'numbers', 'operator', 'optparse', 'os', 'os.path', 'ossaudiodev', 'parser', 'pdb', 'pickle', 'pickletools', 'pipes', 'PixMapWrapper', 'pkgutil', 'platform', 'plistlib', 'popen2', 'poplib', 'posix', 'posixfile', 'pprint', 'profile', 'pstats', 'pty', 'pwd', 'py_compile', 'pyclbr', 'pydoc', 'Queue', 'quopri', 'random', 're', 'readline', 'repr', 'resource', 'rexec', 'rfc822', 'rlcompleter', 'robotparser', 'runpy', 'sched', 'ScrolledText', 'select', 'sets', 'sgmllib', 'sha', 'shelve', 'shlex', 'shutil', 'signal', 'SimpleHTTPServer', 'SimpleXMLRPCServer', 'site', 'smtpd', 'smtplib', 'sndhdr', 'socket', 'SocketServer', 'spwd', 'sqlite3', 'ssl', 'stat', 'statvfs', 'string', 'StringIO', 'stringprep', 'struct', 'subprocess', 'sunau', 'sunaudiodev', 'SUNAUDIODEV', 'symbol', 'symtable', 'sys', 'sysconfig', 'syslog', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'termios', 'test', 'test.test_support', 'textwrap', 'thread', 'threading', 'time', 'timeit', 'Tix', 'Tkinter', 'token', 'tokenize', 'trace', 'traceback', 'ttk', 'tty', 'turtle', 'types', 'unicodedata', 'unittest', 'urllib', 'urllib2', 'urlparse', 'user', 'UserDict', 'UserList', 'UserString', 'uu', 'uuid', 'videoreader', 'W', 'warnings', 'wave', 'weakref', 'webbrowser', 'whichdb', 'winsound', 'wsgiref', 'wsgiref.handlers', 'wsgiref.headers', 'wsgiref.simple_server', 'wsgiref.util', 'wsgiref.validate', 'xdrlib', 'xml', 'xml.dom', 'xml.dom.minidom', 'xml.dom.pulldom', 'xml.etree.ElementTree', 'xml.parsers.expat', 'xml.sax', 'xml.sax.handler', 'xml.sax.saxutils', 'xml.sax.xmlreader', 'xmlrpclib', 'zipfile', 'zipimport', 'zlib',]
        self.modules = set()
        # self.get_builtin_packages()

    def get_builtin_packages(self):
        # html = urllib2.urlopen('http://docs.python.org/2.7/py-modindex.html').read()
        # soup = BeautifulSoup(html)
        # module_elems = soup.find_all(class_='xref')

        # for module_elem in module_elems:
        #     self.builtin_modules.append(module_elem.text)
        fp = open('builtin_packages.txt', 'r')
        for line in fp:
            self.builtin_modules.append(line.strip())
        fp.close()


    def extract_in_file(self, fp):
        if fp[-2:] == 'py':
            log_err('Parsing %s...' % fp)
        else:
            return

        fp_opener = open(fp, 'r')

        multiline_import = False
        comment_flag = False

        for line in fp_opener:
            line = line.strip()

            # Detect comment 
            if line and line[0] == '#': #inline1
                continue
            if len(line)>=6 and (line[:3] == '\'\'\'' or line[:3] == '\"\"\"') and (line.strip()[-3:] == '\'\'\'' or line[-3:] == '\"\"\"'):    #inline2
                continue
            
            if len(line)>=3 and (line[:3] == '\'\'\'' or line[:3] == '\"\"\"'):
                comment_flag = True
                continue
            if comment_flag and len(line)>=3 and (line.strip()[-3:] == '\'\'\'' or line[-3:] == '\"\"\"'):
                comment_flag = False
                continue

            if comment_flag:
                continue

            line_tokens = line.split()

            if line_tokens and (line_tokens[0] == 'import' or multiline_import):
                if multiline_import:
                    imported = ' '.join(line_tokens).strip()    
                else:
                    imported = ' '.join(line_tokens[1:]).strip()

                if line.strip()[-1] == '\\':    #consider next line also
                    multiline_import = True
                else:
                    multiline_import = False

                comma_split_tokens = imported.split(',')
                for comma_split_token in comma_split_tokens:
                    candidate = comma_split_token.strip().split('.')[0].split()[0]
                    if candidate and candidate not in self.builtin_modules:
                        self.modules.add(candidate)
                        
                        if candidate == '0':
                            print fp
                    
            elif line_tokens and line_tokens[0] == 'from':
                candidate = line_tokens[1].split('.')[0]
                if candidate and candidate not in self.builtin_modules:
                    self.modules.add(line_tokens[1].split('.')[0])
                    
                    if candidate == '0':
                        print fp

        fp_opener.close()

    def extract_in_dir(self, fp):
        contents = listdir(fp)
        if fp[-1] != '/':
            fp = fp + '/'
        for content in contents:
            if isdir(fp+content):
                self.extract_in_dir(fp+content)
            else:
                self.extract_in_file(fp+content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--recursive', action='store_true', help='recursive extract under the directory')
    parser.add_argument('fp', help='either a file or a folder where you want to extract dependencies')
    args = parser.parse_args()
    
    fp = args.fp

    if not lexists(fp):
        log_err('[Error] "%s" does not exist.' % fp)
        exit(1)
    
    extractor = DependencyExtracter()
    if args.recursive:
        if not isdir(fp):
            log_err('[Error] "%s" is not a directory.' % fp)
            exit(1)
        else:
            extractor.extract_in_dir(fp)
            return extractor.modules
    else:   #single file
        if isdir(fp):
            log_err('[Error] "%s" is a directory, try to use -r flag.' % fp)
            exit(1)
        else:
            extractor.extract_in_file(fp)
            return extractor.modules


if __name__ == '__main__':
    print main()