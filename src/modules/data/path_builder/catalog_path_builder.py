from typing import Optional


class CatalogPathBuilder():
    def __init__(self, environment: str, layer_config: dict[str, str]):
        self._environment = environment
        self._layer_config = layer_config

    def build(
        self,
        data_layer: Optional[str] = None,
        data_name: Optional[str] = None,
        data_path: Optional[list[str]] = None
    ) -> str:
        if (
            (data_path)
            and (len(data_path) == 3)
        ):
            return f"{self._environment}_{'.'.join(data_path)}"
        
        if (
            (data_layer)
            and (data_name)
        ):
            return f"{self._environment}_{self._layer_config[data_layer]}.{data_name}"
        
        if (
            data_name
        ):
            return data_name

        raise ValueError("Invalid input: Provide a data_path with length 3, or both data_layer and data_name, or at least data_name.")