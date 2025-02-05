from pydantic import BaseModel, ConfigDict
from tree_sitter import Language, Parser


class TSGrammarModel(BaseModel):
    lang: Language
    parser: Parser

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra='forbid',
        frozen=True
    )
