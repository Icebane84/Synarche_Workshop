builtins_path = r"c:\Users\Chris\Synarche_Workspace\stubs\builtins.pyi"

with open(builtins_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip_until = -1

for i, line in enumerate(lines):
    if i <= skip_until:
        continue

    # Target the block we added or the original fromkeys in the dict class
    if "# Signature of `dict.fromkeys` refined" in line or (
        3500 < i < 3700 and "def fromkeys(cls," in line
    ):
        new_lines.append("    @classmethod\n")
        new_lines.append("    @overload\n")
        new_lines.append(
            "    def fromkeys(cls, iterable: Iterable[_T], value: None = None, /) -> Self: ...\n"
        )
        new_lines.append("    @classmethod\n")
        new_lines.append("    @overload\n")
        new_lines.append(
            "    def fromkeys(cls, iterable: Iterable[_T], value: _S, /) -> Self: ...\n"
        )

        # Advance skip_until to skip the existing fromkeys overloads
        j = i + 1
        while j < len(lines) and (
            not lines[j].strip().startswith("def ") or "fromkeys" in lines[j]
        ):
            j += 1
        skip_until = j - 1
        continue

    new_lines.append(line)

with open(builtins_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Builtins patch simplified.")
