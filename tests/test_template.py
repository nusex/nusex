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

import pytest  # type: ignore

from nusex import Template
from nusex.errors import AlreadyExists, TemplateError


def test_validate_template_names():
    bad_templates = ("test-template", "TestTemplate", "folder/test")
    good_templates = ("test", "test_template", "test69")

    for t in bad_templates:
        with pytest.raises(TemplateError) as exc:
            Template(t)
        assert f"{exc.value}" == (
            "Names can only contain lower case letters, numbers, and "
            "underscores"
        )

    for t in good_templates:
        template = Template(t)
        assert template.name == t

    with pytest.raises(TemplateError) as exc:
        Template("this_is_a_really_long_template_name")
    assert f"{exc.value}" == "Names are limited to 24 characters"


def test_reject_reserved_names():
    bad_templates = ("nsx_complex_pkg", "nsx_simple_ext")

    for t in bad_templates:
        with pytest.raises(TemplateError) as exc:
            Template(t)
        assert f"{exc.value}" == "That name is reserved"


def test_reject_taken_names():
    with pytest.raises(AlreadyExists) as exc:
        Template("default")
    assert f"{exc.value}" == "A profile is already using that name"
