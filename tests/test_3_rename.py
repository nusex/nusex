import os
import subprocess as sp
import sys

from nusex import CONFIG_DIR


def run(command):
    if sys.version_info >= (3, 7, 0):
        return sp.run(command, shell=True, capture_output=True)

    if os.name != "nt":
        return sp.run(f"{command} > /dev/null 2>&1", shell=True)

    # Windows users will have to put up with the output for 3.6 tests.
    return sp.run(command, shell=True)


def test_check_template_exists():
    output = run("nsx rename this_template_doesnt_exist test420")
    if sys.version_info < (3, 7, 0):
        assert output.returncode == 1
    else:
        error = output.stderr.decode().split("\n")[-2].strip()
        assert error == (
            "nusex.errors.NoMatchingTemplates: no template named "
            "'this_template_doesnt_exist' exists"
        )


def test_validate_template_names():
    bad_templates = ("test-template", "TestTemplate", "folder/test")
    good_templates = ("test", "test_template", "test69")
    new_good_templates = ("testing", "renamed_template", "test420")

    for tn in bad_templates:
        output = run(f"nsx rename test {tn}")
        if sys.version_info < (3, 7, 0):
            assert output.returncode == 1
        else:
            error = output.stderr.decode().split("\n")[-2].strip()
            assert error == (
                "nusex.errors.TemplateRenameError: template names can only "
                "contain lower case letters, numbers, and underscores"
            )

    for ton, tnn in zip(good_templates, new_good_templates):
        output = run(f"nsx rename {ton} {tnn}")
        if output.returncode != 0:
            assert False, output.stderr.decode().split("\n")[-2].strip()

    for tn in new_good_templates:
        assert os.path.isfile(CONFIG_DIR / f"{tn}.nsx")
