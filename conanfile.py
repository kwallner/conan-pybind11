from conans import ConanFile, tools, CMake
import os


class PyBind11Conan(ConanFile):
    name = "pybind11"
    version = "2.5.0"
    description = "Seamless operability between C++11 and Python"
    topics = "conan", "pybind11", "python", "binding"
    homepage = "https://github.com/pybind/pybind11"
    license = "BSD-3-Clause"
    url = "https://github.com/conan-community/conan-pybind11"
    exports_sources = "CMakeLists.txt"
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"
    no_copy_source = True
    
    def requirements(self):
        self.requires("python/3.7.8@%s/%s" % (self.user, self.channel))
        
    def source(self):
        tools.get("%s/archive/v%s.tar.gz" % (self.homepage, self.version))

    def build(self):
        cmake = CMake(self)
        cmake.definitions["PYBIND11_INSTALL"] = True
        cmake.definitions["PYBIND11_TEST"] = False
        cmake.definitions["PYBIND11_CMAKECONFIG_INSTALL_DIR"] = "lib/cmake/pybind11"
        cmake.configure(source_folder="pybind11-%s" % self.version)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("LICENSE")
        os.unlink(os.path.join(self.package_folder, "lib", "cmake", "pybind11", "pybind11Config.cmake"))
        os.unlink(os.path.join(self.package_folder, "lib", "cmake", "pybind11", "pybind11ConfigVersion.cmake"))

    def package_id(self):
        self.info.header_only()

    def package_info(self):
        self.cpp_info.includedirs.append(os.path.join(self.package_folder, "include", "pybind11"))
        cmake_base_path = os.path.join("lib", "cmake", "pybind11")
        self.cpp_info.builddirs = [cmake_base_path]
        self.cpp_info.build_modules = [os.path.join(cmake_base_path, "FindPythonLibsNew.cmake"),
                                       os.path.join(cmake_base_path, "pybind11Tools.cmake")]
