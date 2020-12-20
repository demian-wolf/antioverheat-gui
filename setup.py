#!/usr/bin/env python

from distutils.core import setup


setup(name="AntiOverheat-GUI",
      version="0.1",
      description="A cpupower and lm_sensors GUI wrapper that might be"
                  "helpful for CPU overheat prevention on Linux systems.",
      author="Demian Volkov",
      author_email="demianwolfssd@gmail.com",
      url="https://github.com/demian-wolf/AntiOverheat-GUI",
      packages=["antioverheat_gui"],
      install_requires=["colour", "pysensors"]
     )
