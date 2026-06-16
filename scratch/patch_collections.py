collections_path = r"c:\Users\Chris\Synarche_Workspace\stubs\collections\__init__.pyi"

with open(collections_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip_until = -1

for i, line in enumerate(lines):
    if i <= skip_until:
        continue

    # UserDict.fromkeys (around line 88)
    if (
        "def fromkeys(cls, iterable: Iterable[_T], value: None = None) -> UserDict[_T, Any | None]:"
        in line
    ):
        new_lines.append("    @classmethod\n")
        new_lines.append("    @overload\n")
        new_lines.append(
            "    def fromkeys(cls, iterable: Iterable[_T], value: None = None) -> Self: ...\n"
        )
        skip_until = i + 4  # skip the next overload too
        new_lines.append("    @classmethod\n")
        new_lines.append("    @overload\n")
        new_lines.append(
            "    def fromkeys(cls, iterable: Iterable[_T], value: _S) -> Self: ...\n"
        )
        continue

    # OrderedDict.fromkeys (around line 451)
    if (
        "def fromkeys(cls, iterable: Iterable[_T], value: None = None) -> OrderedDict[_T, Any | None]:"
        in line
    ):
        new_lines.append("    @classmethod\n")
        new_lines.append("    @overload\n")
        new_lines.append(
            "    def fromkeys(cls: type[OrderedDict[Any, Any]], iterable: Iterable[_T], value: None = None) -> OrderedDict[_T, Any | None]:\n"
        )
        new_lines.append(
            '        """Create a new ordered dictionary with keys from iterable and values set to value."""\n'
        )
        new_lines.append("        ...\n")
        new_lines.append("    @classmethod\n")
        new_lines.append("    @overload\n")
        new_lines.append(
            "    def fromkeys(cls: type[OrderedDict[Any, Any]], iterable: Iterable[_T], value: _S) -> OrderedDict[_T, _S]:\n"
        )
        new_lines.append(
            '        """Create a new ordered dictionary with keys from iterable and values set to value."""\n'
        )
        new_lines.append("        ...\n")
        new_lines.append("    @classmethod\n")
        new_lines.append("    @overload\n")
        new_lines.append(
            "    def fromkeys(cls, iterable: Iterable[_T], value: None = None) -> Self:\n"
        )
        new_lines.append(
            '        """Create a new ordered dictionary with keys from iterable and values set to value."""\n'
        )
        new_lines.append("        ...\n")
        skip_until = i + 8  # skip the next overload too
        new_lines.append("    @classmethod\n")
        new_lines.append("    @overload\n")
        new_lines.append(
            "    def fromkeys(cls, iterable: Iterable[_T], value: _S) -> Self:\n"
        )
        new_lines.append(
            '        """Create a new ordered dictionary with keys from iterable and values set to value."""\n'
        )
        new_lines.append("        ...\n")
        continue

    # ChainMap.fromkeys (around line 630)
    # This one is trickier due to sys.version_info check
    if (
        "def fromkeys(cls, iterable: Iterable[_T], /) -> ChainMap[_T, Any | None]:"
        in line
    ):
        new_lines.append(
            "        def fromkeys(cls, iterable: Iterable[_T], /) -> Self: ...\n"
        )
        continue
    if "def fromkeys(cls, iterable: Iterable[_T]) -> ChainMap[_T, Any | None]:" in line:
        new_lines.append(
            "        def fromkeys(cls, iterable: Iterable[_T]) -> Self: ...\n"
        )
        continue
    if (
        "def fromkeys(cls, iterable: Iterable[_T], value: None, /) -> ChainMap[_T, Any | None]:"
        in line
    ):
        new_lines.append(
            "    def fromkeys(cls, iterable: Iterable[_T], value: None, /) -> Self: ...\n"
        )
        continue
    if (
        "def fromkeys(cls, iterable: Iterable[_T], value: _S, /) -> ChainMap[_T, _S]:"
        in line
    ):
        new_lines.append(
            "    def fromkeys(cls, iterable: Iterable[_T], value: _S, /) -> Self: ...\n"
        )
        continue

    new_lines.append(line)

with open(collections_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Collections patch applied successfully.")
