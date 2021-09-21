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


class NusexError(Exception):
    """The base exception class for nusex."""


class DownloadFailure(NusexError):
    """A download failed."""


class BuildError(NusexError):
    """Building a template failed."""


class InvalidFormat(NusexError):
    """A invalid file has been passed to a decoder."""


class UnsupportedFile(NusexError):
    """A file is not supported in templates (normally due to file size
    restrictions)."""


class NusexUserError(NusexError):
    """An error occurred due to user error."""


class InvalidRequest(NusexUserError):
    """The user request is invalid."""


class InvalidConfiguration(NusexUserError):
    """An entity is incorrectly configured, or a problem has been caused
    directly by an invalid configuration."""


class InvalidName(NusexUserError):
    """A entity name is invalid."""


class AlreadyExists(NusexUserError):
    """The entity already exists."""


class DeploymentConflict(NusexUserError):
    """The template has already been deployed."""


class TemplateNotFound(NusexUserError):
    """The requested template could not be found."""
