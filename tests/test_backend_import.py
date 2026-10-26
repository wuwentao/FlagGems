# Copyright 2026 FlagOS Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from flag_gems.runtime import backend


def _missing_module(name):
    error = ModuleNotFoundError(f"No module named '{name}'")
    error.name = name
    return error


@pytest.mark.parametrize("missing_module", ["_vendor", "_vendor.ops"])
def test_import_module_safe_allows_missing_optional_module(
    monkeypatch, capsys, missing_module
):
    def import_module(_):
        raise _missing_module(missing_module)

    monkeypatch.setattr(backend.importlib, "import_module", import_module)

    assert backend._import_module_safe("_vendor.ops", "vendor", "common") is None
    assert "No specialized common operators were found" in capsys.readouterr().out


def test_import_module_safe_rejects_missing_internal_dependency(monkeypatch):
    def import_module(_):
        raise _missing_module("_vendor.ops.missing_dependency")

    monkeypatch.setattr(backend.importlib, "import_module", import_module)

    with pytest.raises(
        RuntimeError,
        match=r"Failed to import vendor extra lib _vendor\.ops.*missing_dependency",
    ) as error:
        backend._import_module_safe("_vendor.ops", "vendor", "common")

    assert isinstance(error.value.__cause__, ModuleNotFoundError)
