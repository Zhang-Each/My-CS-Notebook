import os
import re
import logging

from jinja2 import Template

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page
from mkdocs.structure.files import Files
from mkdocs.utils import copy_file
from mkdocs.utils.meta import get_data

from typing import Any, Dict, Optional, Tuple

PLUGIN_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(PLUGIN_DIR, 'templates/page_statistics.html')

with open(TEMPLATE_DIR, 'r', encoding='utf-8') as file:
    TEMPLATE = file.read()

log = logging.getLogger('mkdocs.mkdocs_statistics_plugin')

class StatisticsPlugin(BasePlugin):
    config_scheme = (
        ('enabled', config_options.Type(bool, default=True)),
        ('pages_placeholder', config_options.Type(str, default=r'\{\{\s*pages\s*\}\}')),
        ('words_placeholder', config_options.Type(str, default=r'\{\{\s*words\s*\}\}')),
        ('codes_placeholder', config_options.Type(str, default=r'\{\{\s*codes\s*\}\}')),
    )

    enabled = True
    pages = 0
    words = 0
    codes = 0

    def on_config(self, config: config_options.Config, **kwargs) -> Dict[str, Any]:
        return config
    
    def on_files(self, files: Files, *, config: config_options.Config) -> Optional[Files]:
        self.pages = len([file.page for file in files.documentation_pages()])
        for file in files.documentation_pages():
            self._count_page(config['docs_dir'] + '/' + file.src_path)
        return files

    def _count_page(self, path: str) -> None:
        with open(path, encoding='utf-8-sig', errors='strict') as f:
            source = f.read()
        markdown, _ = get_data(source)
        self._words_count(markdown)
        return
    
    def on_page_markdown(
        self, markdown: str, page: Page, config: config_options.Config, files, **kwargs
    ) -> str:
        if not self.enabled:
            return markdown
        
        if not self.config.get('enabled'):
            return markdown
        
        if page.meta.get("statistics"):

            log.info(f"pages: {self.pages}, words: {self.words}, codes: {self.codes}")

            markdown = re.sub(
                self.config.get("pages_placeholder"),
                str(self.pages),
                markdown,
                flags=re.IGNORECASE,
            )

            markdown = re.sub(
                self.config.get("words_placeholder"),
                str(self.words),
                markdown,
                flags=re.IGNORECASE,
            )

            markdown = re.sub(
                self.config.get("codes_placeholder"),
                str(self.codes),
                markdown,
                flags=re.IGNORECASE,
            )

        if not page.meta.get("nostatistics"):

            code_lines = 0
            chinese, english, codes = self._split_markdown(markdown)
            words = len(chinese) + len(english.split())
            for code in codes:
                code_lines += len(code.splitlines()) - 2
            
            lines = markdown.splitlines()
            h1 = -1
            for idx, line in enumerate(lines):
                if re.match(r"\s*# ", line):
                    h1 = idx
                    break
            read_time = round(words / 300 + code_lines / 80)
            page_statistics_content = Template(TEMPLATE).render(
                words = words,
                code_lines = code_lines,
                read_time = read_time
            )
            lines.insert(h1 + 1, page_statistics_content)
            markdown = "\n".join(lines)

        return markdown

    def _words_count(self, markdown: str) -> None:
        chinese, english, codes = self._split_markdown(markdown)
        self.words += len(chinese) + len(english.split())
        for code in codes:
            self.codes += len(code.splitlines()) - 2

    def _split_markdown(self, markdown: str) -> tuple:
        markdown, codes = self._clean_markdown(markdown)
        chinese = "".join(re.findall(r'[\u4e00-\u9fa5]', markdown))
        english = " ".join(re.findall(r'[a-zA-Z0-9]*?(?![a-zA-Z0-9])', markdown))
        return chinese, english, codes
    
    def _clean_markdown(self, markdown: str) -> Tuple[str, list]:
        codes = re.findall(r'```[^\n].*?```', markdown, re.S)
        markdown = re.sub(r'```[^\n].*?```', '', markdown, flags=re.DOTALL | re.MULTILINE)
        markdown = re.sub(r'<!--.*?-->', '', markdown, flags=re.DOTALL | re.MULTILINE)
        markdown = markdown.replace('\t', '    ')
        markdown = re.sub(r'[ ]{2,}', '    ', markdown)
        markdown = re.sub(r'^\[[^]]*\][^(].*', '', markdown, flags=re.MULTILINE)
        markdown = re.sub(r'{#.*}', '', markdown)
        markdown = markdown.replace('\n', ' ')
        markdown = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', markdown)
        markdown = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', markdown)
        markdown = re.sub(r'</?[^>]*>', '', markdown)
        markdown = re.sub(r'[#*`~\-–^=<>+|/:]', '', markdown)
        markdown = re.sub(r'\[[0-9]*\]', '', markdown)
        markdown = re.sub(r'[0-9#]*\.', '', markdown)
        return markdown, codes