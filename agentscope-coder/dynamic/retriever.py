"""retriever.py - Template matching for static layer

Simplified version of tutorial_generator/retriever.py
"""

import json
import os
import re
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class TemplateInfo:
    """Template metadata"""
    id: str
    title: str
    category: str
    keywords: List[str]
    concise_path: str
    minimal_path: Optional[str] = None
    complete_path: Optional[str] = None


class TemplateRetriever:
    """Fast template matching by keywords"""

    def __init__(self, templates_dir: str = None):
        if templates_dir is None:
            templates_dir = os.path.join(
                os.path.dirname(__file__),
                "..", "references", "templates"
            )
        self.templates_dir = os.path.expanduser(templates_dir)
        self.templates: Dict[str, TemplateInfo] = {}
        self.keyword_index: Dict[str, List[str]] = {}
        self._load_templates()

    def _load_templates(self):
        """Load metadata from metadata_index.json"""
        index_path = os.path.join(self.templates_dir, "metadata_index.json")
        if not os.path.exists(index_path):
            return

        with open(index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for tpl in data.get("templates", []):
                # Find template directory
                category = tpl.get("category", "")
                tpl_id = tpl.get("id", "")
                tpl_dir = os.path.join(self.templates_dir, category, tpl_id)

                info = TemplateInfo(
                    id=tpl_id,
                    title=tpl.get("title", ""),
                    category=category,
                    keywords=tpl.get("keywords", []),
                    concise_path=os.path.join(tpl_dir, "concise.py"),
                    minimal_path=os.path.join(tpl_dir, "minimal.py"),
                    complete_path=os.path.join(tpl_dir, "complete.py"),
                )
                self.templates[tpl_id] = info

                # Build keyword index
                for kw in info.keywords:
                    kw_lower = kw.lower()
                    if kw_lower not in self.keyword_index:
                        self.keyword_index[kw_lower] = []
                    self.keyword_index[kw_lower].append(tpl_id)

    def match(self, query: str) -> Optional[TemplateInfo]:
        """Match template by query keywords"""
        query_lower = query.lower()
        words = self._tokenize(query_lower)

        scores = {}
        for word in words:
            if word in self.keyword_index:
                for tpl_id in self.keyword_index[word]:
                    scores[tpl_id] = scores.get(tpl_id, 0) + 1

        if scores:
            best_id = max(scores.keys(), key=lambda x: scores[x])
            if scores[best_id] >= 1:
                return self.templates.get(best_id)
        return None

    def get_template_code(
        self,
        template_id: str,
        complexity: str = "concise"
    ) -> Optional[str]:
        """Get template code by ID and complexity"""
        if template_id not in self.templates:
            return None

        info = self.templates[template_id]
        path_map = {
            "minimal": info.minimal_path,
            "concise": info.concise_path,
            "complete": info.complete_path,
        }

        path = path_map.get(complexity, info.concise_path)
        if path and os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        return None

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize query into keywords"""
        words = []

        # Chinese characters
        for match in re.finditer(r'[\u4e00-\u9fff]+', text):
            words.append(match.group(0))

        # English words - split by space and hyphen
        # First find all continuous sequences of alphanumeric chars
        for match in re.finditer(r'[a-zA-Z0-9_-]+', text.lower()):
            word = match.group(0)
            # Handle underscore/hyphen separated words
            if '_' in word:
                parts = word.split('_')
                words.extend([p for p in parts if len(p) > 1])
            elif '-' in word:
                parts = word.split('-')
                words.extend([p for p in parts if len(p) > 1])
            else:
                if len(word) > 1:
                    words.append(word)

        # Filter stopwords - removed 'agent' from stopwords
        stopwords = {'how', 'to', 'use', 'the', 'a', 'an', 'for', 'with', '如何', '怎么', '使用'}
        return [w for w in words if w not in stopwords and len(w) > 1]
