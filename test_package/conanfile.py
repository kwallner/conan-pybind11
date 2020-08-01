from conans import ConanFile, CMake, tools
import os
import sys
import shutil


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "cmake_find_package"

    def requirements(self):
        self.requires("python/3.7.8@%s/%s" % (self.user, self.channel))

    @property 
    def _python_interpreter(self):
        python_cmd = shutil.which("python3")
        if python_cmd is None:
            python_cmd = shutil.which("python")
        if python_cmd is None:
            raise errors.ConanInvalidConfiguration("Failed to find python executable.")
        return python_cmd

    def build(self):
        cmake = CMake(self)
        cmake.definitions["PYTHON_EXECUTABLE"] = self._python_interpreter
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self.settings):
            with tools.environment_append({"PYTHONPATH": "lib"}):
                self.run("{} {}".format(self._python_interpreter, os.path.join(self.source_folder, "test.py")), run_environment=True)
