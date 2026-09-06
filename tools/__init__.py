from core.registry import ToolRegistry

from tools.examples.example_tool import ExampleTool
from tools.recon.nmap import NmapTool


def create_registry() -> ToolRegistry:
    """
    Create and populate the global tool registry.
    """

    registry = ToolRegistry()

    registry.register(
        ExampleTool()
    )

    registry.register(
        NmapTool()
    )

    return registry