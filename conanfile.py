#!/usr/bin/python
from Azul3DConan import Azul3DConan

class MyCudaConan(Azul3DConan):
    name = "MyCuda"
    version = "0.0.1"

    def requirements(self):
        # WARNNING! DO NOT REMOVE! Beginning of Protected Section
        self.preRequirements(self)
        # WARNNING! DO NOT REMOVE! End of Protected Section

        if not self.options.sdk:
            pass
        else:
            pass

    def package(self):
        # WARNNING! DO NOT REMOVE! Beginning of Protected Section
        self.prePackage()
        # WARNNING! DO NOT REMOVE! End of Protected Section

    def package_info(self):
        pass
