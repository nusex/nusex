# Copyright (c) 2021, Ethan Henderson
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import platform

import nusex

BANNER = """
      ::::    ::: :::    :::  ::::::::  :::::::::: :::    :::
     :+:+:   :+: :+:    :+: :+:    :+: :+:        :+:    :+:
    :+:+:+  +:+ +:+    +:+ +:+        +:+         +:+  +:+
   +#+ +:+ +#+ +#+    +:+ +#++:++#++ +#++:++#     +#++:+
  +#+  +#+#+# +#+    +#+        +#+ +#+         +#+  +#+
 #+#   #+#+# #+#    #+# #+#    #+# #+#        #+#    #+#
###    ####  ########   ########  ########## ###    ###

"""


def display_splash() -> None:
    print(
        f"{BANNER}"
        f"{nusex.__description__}\n\n"
        f"You're using version {nusex.__version__}.\n\n"
        "I've got nothing to do! Try one of the following:\n\n"
        "  - nusex init          • Initialise the nusex CLI\n"
        "  - nusex build <name>  • Build a template from the current directory\n"
        "  - nusex deploy <name> • Deploy a template to the current directory\n"
        "  - nusex --info        • Display useful information\n\n"
        f"Visit {nusex.__docs__} or use `nusex --help` "
        "to find out how to use nusex.\n\n"
        "Thanks for using nusex!"
    )


def display_info() -> None:
    py_impl = platform.python_implementation()
    py_ver = platform.python_version()
    py_comp = platform.python_compiler()
    system = platform.system()
    release = platform.release()

    if system == "Linux":
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("PRETTY_NAME"):
                    d = line.split("=")[1].strip().replace('"', "")
                    distro = f"\n└──{d}"
                    break
    else:
        distro = ""

    print(
        f"nusex {nusex.__version__}\n"
        f"{py_impl} {py_ver} {py_comp}\n"
        f"{system} {release} {distro}"
    )
