import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from data_classes import Model
from cache import InMemoryCache


class Ollama:
    def __init__(self, link: str = "https://ollama.com/library", cache_hours: float = 12) -> None:
        self.link = link
        self.cache = InMemoryCache(ttl_hours=cache_hours)

    # =============================================================================
    # Public methods - Use these methods to interact with the Ollama class
    # =============================================================================

    def get_models(self) -> List[Model]:
        return self.cache.get("models", self._fetch_and_parse_models)
    
    def _fetch_and_parse_models(self) -> List[Model]:
        model_elements = self._parse_models()
        models = []
        for element in model_elements:
            model = self._extract_model_data(element)
            models.append(model)
        return models

    def get_models_json(self) -> List[Dict]:
        models = self.get_models()
        return [model.to_dict() for model in models]

    def get_model_by_name(self, name: str) -> Optional[Model]:
        models = self.get_models()
        for model in models:
            if model.title.lower() == name.lower():
                return model
        return None

    def get_models_by_capability(self, capability: str) -> List[Model]:
        models = self.get_models()
        return [
            model
            for model in models
            if capability.lower() in [c.lower() for c in model.capabilities]
        ]

    def get_models_by_size(self, size: str) -> List[Model]:
        models = self.get_models()
        return [
            model
            for model in models
            if size.lower() in [s.lower() for s in model.sizes]
        ]
    
    def get_cache_status(self) -> dict:
        return self.cache.get_cache_info("models")

    # =============================================================================
    # Internal helper methods - Do not call these methods directly
    # =============================================================================

    def _fetch_content(self):
        r = requests.get(self.link)
        text = r.text
        return text

    def _parse_models(self):
        html = self._fetch_content()
        soup = BeautifulSoup(html, "html.parser")
        return soup.select("#repo li")

    def _extract_model_data(self, model_element) -> Model:
        # Extract model title
        title_elem = model_element.select_one("h2 span")
        title = title_elem.get_text().strip() if title_elem else "N/A"

        # Extract description
        desc_elem = model_element.select_one("p.text-neutral-800")
        description = desc_elem.get_text().strip() if desc_elem else "N/A"

        # Extract parameters/sizes
        size_elems = model_element.select("span[x-test-size]")
        sizes = [elem.get_text().strip() for elem in size_elems]

        # Extract capabilities
        capability_elems = model_element.select("span[x-test-capability]")
        capabilities = [elem.get_text().strip() for elem in capability_elems]

        # Extract stats (pulls, tags, updated)
        pull_elem = model_element.select_one("span[x-test-pull-count]")
        pulls = pull_elem.get_text().strip() if pull_elem else "N/A"

        tag_elem = model_element.select_one("span[x-test-tag-count]")
        tags = tag_elem.get_text().strip() if tag_elem else "N/A"

        updated_elem = model_element.select_one("span[x-test-updated]")
        updated = updated_elem.get_text().strip() if updated_elem else "N/A"

        return Model(
            title=title,
            description=description,
            sizes=sizes,
            capabilities=capabilities,
            pulls=pulls,
            tags=tags,
            updated=updated,
        )
