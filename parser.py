"""
Purist Parser, entry point to parse the purist source code
"""
import sys

from typing import List
from lexer import Token, Tokenizer

class Node():
    """
    Abstract Syntax Tree Node
    """
    pass

class Parser():
    """
    Purist Parser, once it has tokens it checks if the tokens can form a valid AST
    """
    def __init__(self) -> None:
        self._tokenizer = Tokenizer()

    def parse(self, file_path: str) -> Node:
        """
        Parse a file and return a root Node of the AST

        Args:
            file_path: path to the file to parse
        Returns:
            Node: an abstract syntax tree root node
        """
        with open(file_path, 'r') as file:
            text = file.read()
            tokens = self._tokenizer.tokenize(file_path, text)
            ast = self._parse_tokens(tokens)
            return ast

    def _parse_tokens(self, tokens: List[Token]) -> Node:
        for token in tokens:
            print(token)
        return Node()

def main(filename: str) -> None:
    """
    Entry point to the parser
    """
    parser = Parser()
    parser.parse(f'purist-src/{filename}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python parser.py <filename>')
        print('the source code paths is currently relative to the purity-src folder')
        print('example usage: python parser.py entry.purist')
        sys.exit(1)
    main(sys.argv[1])
