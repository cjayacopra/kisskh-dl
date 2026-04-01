from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, RootModel, model_validator


class SubItem(BaseModel):
    file: Optional[str] = None
    label: str
    kind: str = "captions"

    @model_validator(mode="before")
    @classmethod
    def handle_src_or_file(cls, data):
        if isinstance(data, dict):
            if data.get("src") is not None and data.get("file") is None:
                data["file"] = data["src"]
            elif data.get("file") is not None and data.get("src") is None:
                data["file"] = data["file"]
        return data


class Sub(RootModel[List[SubItem]]):
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self) -> int:
        return len(self.root)
