import hashlib
import orjson


class ParserEngine:

    def parse(self, source: str):

        # Placeholder parser.
        # Later this becomes a full grammar parser using Lark.

        return {
            "ast_version": 1,
            "source_hash": hashlib.sha256(
                source.encode()
            ).hexdigest(),
            "nodes": [],
            "edges": [],
            "length": len(source),
        }

    def serialize(self, ast):

        return orjson.dumps(ast).decode()