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

from nusex import checks
from tests import DATA_DIR


def test_is_initialised() -> None:
    # Not a whole lot I can do here.
    assert checks.is_initialised() == False


def test_name_is_valid_pass() -> None:
    assert checks.name_is_valid("valid_name") == True


def test_name_is_valid_fail() -> None:
    assert checks.name_is_valid("CapitalName") == False
    assert checks.name_is_valid("this_name_is_not_valid_because_its_long") == False
    assert checks.name_is_valid("kebab-case") == False


def test_does_not_conflict_pass() -> None:
    assert checks.does_not_conflict("free", in_dir=DATA_DIR, extension="json") == True
    assert (
        checks.does_not_conflict("free", in_dir=str(DATA_DIR), extension="json") == True
    )


def test_does_not_conflict_fail() -> None:
    assert (
        checks.does_not_conflict("stored_profile", in_dir=DATA_DIR, extension="json")
        == False
    )
