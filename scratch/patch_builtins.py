import os

builtins_path = r"c:\Users\Chris\Synarche_Workspace\stubs\builtins.pyi"

with open(builtins_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_until = -1

for i, line in enumerate(lines):
    if i <= skip_until:
        continue
    
    # dict.copy replacement (around 3563)
    if 'def copy(self) -> dict[_KT, _VT]:' in line:
        new_lines.append('    def copy(self) -> Self:\n')
        continue
    
    # dict.fromkeys replacement (around 3575)
    if '# Signature of `dict.fromkeys` should be kept identical to' in line:
        new_lines.append('    # Signature of `dict.fromkeys` refined to support subclass type inference.\n')
        new_lines.append('    # Base dict case is handled via specific overloads to maintain parameter precision.\n')
        new_lines.append('    # Subclass cases use Self to ensure the derived class type is preserved.\n')
        new_lines.append('    @classmethod\n')
        new_lines.append('    @overload\n')
        new_lines.append('    def fromkeys(cls: type[dict[Any, Any]], iterable: Iterable[_T], value: None = None, /) -> dict[_T, Any | None]:\n')
        new_lines.append('        """Create a new dictionary with keys from iterable and values set to value."""\n')
        new_lines.append('        ...\n')
        new_lines.append('    @classmethod\n')
        new_lines.append('    @overload\n')
        new_lines.append('    def fromkeys(cls: type[dict[Any, Any]], iterable: Iterable[_T], value: _S, /) -> dict[_T, _S]:\n')
        new_lines.append('        """Create a new dictionary with keys from iterable and values set to value."""\n')
        new_lines.append('        ...\n')
        new_lines.append('    @classmethod\n')
        new_lines.append('    @overload\n')
        new_lines.append('    def fromkeys(cls, iterable: Iterable[_T], value: None = None, /) -> Self:\n')
        new_lines.append('        """Create a new dictionary with keys from iterable and values set to value."""\n')
        new_lines.append('        ...\n')
        new_lines.append('    @classmethod\n')
        new_lines.append('    @overload\n')
        new_lines.append('    def fromkeys(cls, iterable: Iterable[_T], value: _S, /) -> Self:\n')
        new_lines.append('        """Create a new dictionary with keys from iterable and values set to value."""\n')
        new_lines.append('        ...\n')
        
        # Skip original fromkeys lines
        # Original lines 3575 to 3588 (14 lines)
        # We find the end of the fromkeys method
        for j in range(i + 1, len(lines)):
            if 'def fromkeys' in lines[j] and 'value: _S' in lines[j]:
                skip_until = j + 2 # Skip the ... line too
                break
        continue

    new_lines.append(line)

with open(builtins_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Patch applied successfully.")
