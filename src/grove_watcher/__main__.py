import logging

from .config.logger_loader import setup_logging
from .ts_lang_fetcher import TreeSitterInit, VenvManager

setup_logging()

def find(language: str, use_venv: bool = False):
    language = language.lower().strip()
    venv_manager = VenvManager() if use_venv else None
    tree_sitter = TreeSitterInit(venv_manager)
    logging.info(f"Attempting to initialize Tree-sitter parser for '{language}'...")

    try:
        ts_grammar = tree_sitter.get_grammar(language)
        logging.debug(f"Tree sitter lang/parser pydantic object: {ts_grammar}")
        logging.info(
            f"Tree sitter grammar object for {language} language is generated successfully."
        )
        return ts_grammar
    except Exception as e:
        logging.error(f"Failed to initialize grammar object for '{language}': {e}")
        return None
