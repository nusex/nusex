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

from nusex.errors import InvalidFormat, UnsupportedFile

SPEC_ID = b"\x99\x78"


class NSXEncoder:
    def write(self, path, data):
        with open(path, "wb") as f:
            # Identify format.
            f.write(SPEC_ID)

            # Write headers.
            ef = data["extension_for"]
            if ef:
                f.write(b"\x01")
                f.write(ef.ljust(24).encode())
            else:
                f.write(b"\x00")

            f.write(b"\x00" * 9)  # Reserved space.

            # Files chunk starting byte.
            f.write(b"\x01")
            for k, v in data["files"].items():
                f.write(k.encode())
                f.write(b"\x97")
                size = len(v)
                if size > 536_870_912:
                    raise UnsupportedFile(
                        "Files larger than 512 MiB are not supported"
                    )
                f.write(f"{len(v)}".ljust(9).encode())
                f.write(v)
            f.write(b"\x98")

            # Installs chunk starting byte.
            f.write(b"\x02")
            for i in data["installs"]:
                f.write(i.encode())
                f.write(b"\x97")
            f.write(b"\x98")


class NSXDecoder:
    def __init__(self):
        self.defaults = {
            "files": {},
            "installs": [],
            "extension_for": "",
        }

    def _process_files(self, f, data):
        key = True
        name = b""

        while True:
            if key:
                chunk = f.read(1)

                if chunk == b"\x97":
                    key = False
                    continue

                if chunk == b"\x98":
                    return data

                name += chunk

            else:
                size = int(f.read(9).decode().strip())
                chunk = f.read(size)
                data["files"].update({name.decode(): chunk})
                name = b""
                key = True

    def _process_installs(self, f, data):
        inst = b""
        while True:
            b = f.read(1)
            if b == b"\x98":
                return data

            if b == b"\x97":
                data["installs"].append(inst.decode())
                inst = b""
                continue

            inst += b

    def read(self, path):
        data = self.defaults.copy()
        with open(path, "rb") as f:
            # Validate format.
            if f.read(2) != SPEC_ID:
                raise InvalidFormat("Not a valid NSX file")

            # Read headers.
            ef = f.read(1)
            if ef == b"\x01":
                data["extension_for"] = f.read(24).decode().strip()

            f.read(9)  # Skip reserved.

            # Process chunks.
            while f.peek(1):
                data = {
                    b"\x01": self._process_files,
                    b"\x02": self._process_installs,
                }[f.read(1)](f, data)

        return data