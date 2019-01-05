from conans import ConanFile, tools
import os

from os import unlink


class AndroidNdkConan(ConanFile):
    name = "android-ndk"
    version = "r17b"
    license = "GPL/APACHE2"
    url = "https://github.com/conan-mobile/conan-android-ndk.git"
    settings = None
    options = {"host_os": ["Linux", "Windows", "Macos"], "host_arch": ["x86", "x86_64"]}
    description = "Conan Package for the Android NDK toolchain"
    short_paths = True
 
    def config_options(self):
        os_info = tools.OSInfo()
        if os_info.is_linux:
            self.options.host_os = "Linux"
        elif os_info.is_windows:
            self.options.host_os = "Windows"
        elif os_info.is_macos:
            self.options.host_os = "Macos"
        else:
            raise Exception("Unsupported platform")

        import sys
        is_64bits = sys.maxsize > 2 ** 32
        if is_64bits:
            self.options.host_arch = "x86_64"
        else:
            self.options.host_arch = "x86"

    def source(self):

        urls = {"Windows_x86_64": ["https://dl.google.com/android/repository/android-ndk-%s-windows-x86_64.zip" % self.version,
                                   "71d2ba2f1618a27a629ce019fc8e46f28ffdd49f"],
                "Windows_x86": ["https://dl.google.com/android/repository/android-ndk-%s-windows-x86.zip" % self.version,
                                "41e4720fc10a993a336c7b416474bc3e1f8fb1e9"],
                "Macos_x86_64": ["https://dl.google.com/android/repository/android-ndk-%s-darwin-x86_64.zip" % self.version,
                                 "f990aafaffec0b583d2c5420bfa622e52ac14248"],
                "Linux_x86_64": ["https://dl.google.com/android/repository/android-ndk-%s-linux-x86_64.zip" % self.version,
                                 "dd5762ee7ef4995ad04fe0c45a608c344d99ca9f"]
        }

        try:
            url, sha1 = urls.get("%s_%s" % (self.options.host_os, self.options.host_arch))
        except KeyError:
            raise Exception("Not supported OS or architecture: ")

        tools.download(url, "ndk.zip")
        tools.check_sha1("ndk.zip", sha1)
        tools.unzip("ndk.zip", keep_permissions=True)
        unlink("ndk.zip")

    @property
    def zip_folder(self):
        return "android-ndk-%s" % self.version

    def package(self):
        self.copy("*", dst="", src=self.zip_folder, keep_path=True)

    def package_info(self):
        tools_path = os.path.join("build", "tools")
        self.cpp_info.bindirs.append(tools_path)
        self.env_info.PATH.append(os.path.join(self.package_folder, tools_path))
