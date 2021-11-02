from typing import Optional, TypeVar, Generic, Any, Iterable, List

from django.apps import AppConfig
from rest_framework.fields import Field

from API.objects import Input
from API.serializers.OutputSerializer import register_output_serializer

T = TypeVar('T')


class E3ModuleConfig(AppConfig, Generic[T]):
    """
    Sets configuration options for an E3 module. This includes the name, its optional dependency, ID of what
    this module outputs, and the serializer field to use for outputting.
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

    def run(self, base_input: Any, dependencies: Optional[dict] = None) -> T:
        """
        Main analysis method. This method will be overridden by an E3 module and include any calculations to create the
        desired output.

        :param base_input: The user provided JSON input.
        :param dependencies: Any previous calculates in the dependency graph.
        :return: The result of the defined calculation.
        """
        pass


class Node:
    """
    Represents a module node in the dependency graph. Contains a reference to each node that is a dependency and pulls
    each dependency from that node when called to run.
    """
    def __init__(self, module: E3ModuleConfig):
        self.dependencies = []
        self.module = module

    def add_dependency(self, node: "Node"):
        """
        Adds the given node as a dependency. It the given module is the same as this module and error is thrown to avoid
        self-dependencies.

        :param node: The node to add as a dependency.
        """
        if node is self:
            raise AssertionError(f"Module outputting {self.module.output} cannot depend on itself")

        self.dependencies.append(node)

    def run(self, base_input: Input, cache: dict):
        """
        Runs the module calculation associated with this node if not in the cache, or pulls from the cache if it has
        been computed previously.

        :param base_input: The input to pass to the calculation function.
        :param cache: The output cache to pull existing data from or store computed results to.
        :return: The result of the module calculation, either from cache or computed.
        """
        if self.module.output in cache:
            return cache[self.module.output]

        result = self.module.run(
            base_input,
            {dep.module.output: dep.run(base_input, cache) for dep in self.dependencies}
        )
        cache[self.module.output] = result

        return result

    def get_str(self):
        """
        Create a string representation of the output of this node. All its dependencies will be recursively resolved
        and included in this node's string representation.

        :return: A string representing the output of this node and its dependencies.
        """
        return f"{[dep.get_str() for dep in self.dependencies]} -> {self.module.output}"


class Singleton(type):
    """
    Metaclass to turn a class into a singleton.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ModuleGraph(metaclass=Singleton):
    """
    Singleton class to maintain the entire module dependency graph. All modules must be added before being run.
    Dependencies will be automatically resolved.
    Note: Modules must not be circularly dependent.
    """
    nodes = {}

    open_nodes: List[Node] = []

    def add_module(self, module: E3ModuleConfig):
        """
        Adds the given E3 module to the dependency graph. All dependencies are automatically resolved.

        :param module: The module to add to the dependency graph.
        """
        if module.output in self.nodes:
            raise ValueError(f"Cannot add module with output {module.output}! Module with this output already exists.")

        new_node = Node(module)
        self.nodes[module.output] = new_node

        # Check if a previously added module resolves this module's dependencies.
        if new_node.module.depends_on is not None:
            for output, node in self.nodes.items():
                if output in new_node.module.depends_on:
                    new_node.add_dependency(node)

            if len(new_node.dependencies) != len(new_node.module.depends_on):
                self.open_nodes.append(new_node)

        # Check if the module being added resolves any open dependencies from a previous module.
        for open_node in self.open_nodes:
            if new_node.module.output in open_node.module.depends_on:
                open_node.add_dependency(new_node)

            if len(open_node.dependencies) == len(open_node.module.depends_on):
                self.open_nodes.remove(open_node)

    def run(self, name: str, base_input: Input, cache: dict):
        """
        Gets the requested output object from its associated module.

        :param name: The name of the object to get.
        :param base_input: The JSON input request.
        :param cache: The result cache as a dictionary.
        :return: The requested object.
        """
        return self.nodes[name].run(base_input, cache)

    def __repr__(self):
        """
        :return: A string representation of the nodes in this dependency graph.
        """
        result = f"ModuleGraph [\n"
        for node in self.nodes.values():
            result += "\t" + node.get_str() + "\n"
        return result + "]"
