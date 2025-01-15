import os
import tempfile

from typing import List, Tuple

import git

from purist.importcompilers.importer import Importer
from purist.parser import Parser
from purist.models.node import Node
from purist.models.token import Token

from utils.errors import InvalidImportStatement, InvalidSyntaxError
from utils.filereader import FileReader
from utils.logger import Logger

class GitImportCompiler(Importer, Parser):
    def __init__(self):
        super().__init__()
        self.__base_path = ""
        self.__requester_file = ""
        self.__requester_line = 0

    def compile(
            self,
            source_path: str,
            requester_file: str|None = None,
            requester_line: int|None = None
    ) -> Node:
        self.__requester_file = requester_file
        self.__requester_line = requester_line
        temp_path = tempfile.gettempdir()
        Logger.trace(f"temp: {temp_path}")
        git_url, git_branch = self._get_url_and_branch(source_path)
        Logger.debug(f"url: {git_url}")
        Logger.debug(f"branch: {git_branch}")

        git_path = os.path.join(temp_path, "purist-git")
        Logger.debug(git_path)
        repo, project_name = self._clone_or_refresh(git_path, git_url, git_branch)
        self.__base_path = git_path

        if source_path.endswith("."):
            error = InvalidSyntaxError(
                "Package name cannot end with a dot!",
                requester_file,
                requester_line,
                0
            )
            raise ValueError(error.get_error())
        reader = FileReader()
        file_path = self._get_source_path_to_compile(source_path)
        Logger.debug(f"file path from url: {file_path}")
        if not file_path.endswith(".purist"):
            Logger.trace(f"base path: [{self.__base_path}/{project_name}]")
            path_parts = file_path.split(".")
            file_path = os.path.join(self.__base_path, project_name)
            Logger.debug(file_path)
            file_path_parts = os.path.join(*path_parts)
            Logger.debug(file_path_parts)
            file_path = os.path.join(file_path, file_path_parts)
            file_path += ".purist"
            Logger.debug(file_path)
        else:
            file_path = os.path.join(self.__base_path, project_name)
            self.__base_path = os.path.dirname(file_path)
            Logger.debug(self.__base_path)
        content = reader.read(file_path)
        tokens = self._tokenizer.tokenize(source_path, content)

        return self.parse(tokens, 0, source_path)

    def parse(
            self,
            tokens: List[Token],
            index: int,
            source_path: str|None = None
    ) -> Tuple[Node, int]:
        Logger.debug(tokens)

    def _get_url_and_branch(self, source_path: str) -> Tuple[str, str]:
        url_parts = source_path.split(":")
        git_branch = "main"
        if "[" in url_parts[1] and "]" in url_parts[1]:
            git_branch = url_parts[1].split("[")[1].split("]")[0]
            url_parts[1] = url_parts[1].split("[")[0].split("]")[0]
        git_url = f"{url_parts[0]}:{url_parts[1]}"
        return git_url, git_branch

    def _clone_or_refresh(self, git_folder: str, git_url: str, branch: str) -> Tuple[git.Repo, str]:
        project_name = ""
        parts = git_url.split("/")
        for part in parts:
            if part.endswith(".git"):
                project_name = part[:-4]
        if len(project_name) == 0:
            error = InvalidImportStatement(self.__requester_file, self.__requester_line, 0)
            raise ValueError(error.get_error())
        git_path = os.path.join(git_folder, project_name)
        Logger.debug(git_path)
        if os.path.exists(git_path):
            return self._refresh(git_path, branch), project_name
        else:
            return self._clone(git_path, git_url, branch), project_name

    def _clone(self, git_folder: str, git_url: str, branch:str) -> git.Repo:
        repo = git.Repo.clone_from(git_url, git_folder)
        repo.git.checkout(branch)

        return repo

    def _refresh(self, git_folder: str, branch: str) -> git.Repo:
        repo = git.Repo(git_folder)
        origin = repo.remote(name='origin')
        origin.pull()
        repo.git.checkout(branch)

        return repo

    def _get_source_path_to_compile(self, source_path: str) -> str:
        url_parts = source_path.split(":")
        return url_parts[-1]
