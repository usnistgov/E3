from typing import Optional, TypeVar, Generic, Any, Iterable

from django.apps import AppConfig
from rest_framework.fields import Field

from API.serializers.OutputSerializer import register_output_serializer

T = TypeVar('T')


class E3AppConfig(AppConfig, Generic[T]):
    """
    Sets configuration options for an E3 module. This includes the name, its optional dependency, and the ID of what
    this module outputs.
    """
    name: str = ""
    depends_on: Optional[Iterable[str]] = None
    output: str = ""
    serializer: Field = None

    def __init__(self, app_name, app_module):
        """
        Registers this module with the registry. Raises an AssertionError if output is not defined.
        """
        super().__init__(app_name, app_module)

        if not self.output:
            raise AssertionError(f"E3 Module must define an output, value was {self.output}")

        ModuleGraph().add_module(self)

        if self.serializer is not None:
            register_output_serializer(self.output, self.serializer)

    def analyze(self, base_input: Any, steps: Optional[dict] = None) -> T:
        """
        Main analysis method. This method will be overridden by an E3 module and include any calculations to create the
        desired output.

        :param base_input: The user provided JSON input.
        :param steps: Any previous calculates in the dependency graph.
        :return: The result of the defined calculation.
        """
        pass


class Node:
    def __init__(self, module: E3AppConfig):
        self.dependencies = []
        self.module = module

    def add_dependency(self, node: "Node"):
        if node is self:
            raise AssertionError(f"Module outputting {self.module.output} cannot depend on itself")

        self.dependencies.append(node)

    def run(self, base_input, cache):
        if self.module.output in cache:
            return cache[self.module.output]

        result = self.module.analyze(
            base_input,
            {dep.module.output: dep.run(base_input, cache) for dep in self.dependencies}
        )
        cache[self.module.output] = result

        return result

    def get_str(self):
        return f"{[dep.get_str() for dep in self.dependencies]} -> {self.module.output}"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ModuleGraph(metaclass=Singleton):
    nodes = {}

    open_nodes: list[Node] = []

    def add_module(self, module: E3AppConfig):
        if module.output in self.nodes:
            raise ValueError(f"Cannot add module with output {module.output}! Module with this output already exists.")

        new_node = Node(module)
        self.nodes[module.output] = new_node

        if new_node.module.depends_on is not None:
            for output, node in self.nodes.items():
                if output in new_node.module.depends_on:
                    new_node.add_dependency(node)

            if len(new_node.dependencies) != len(new_node.module.depends_on):
                self.open_nodes.append(new_node)

        for open_node in self.open_nodes:
            if new_node.module.output in open_node.module.depends_on:
                open_node.add_dependency(new_node)

            if len(open_node.dependencies) == len(open_node.module.depends_on):
                self.open_nodes.remove(open_node)

    def run(self, name, base_input, cache):
        return self.nodes[name].run(base_input, cache)

    def __repr__(self):
        result = f"ModuleGraph [\n"
        for node in self.nodes.values():
            result += "\t" + node.get_str() + "\n"
        return result + "]"
