# AGR Protocol Buffers

All inter-service communication MUST occur through these Protocol Buffer definitions.

Generation example:

```bash
python -m grpc_tools.protoc \
    -I=. \
    --python_out=. \
    --grpc_python_out=. \
    *.proto
```

Future language generators:

- Go
- Rust
- Java
- C#
- TypeScript