from typing import Optional, TypeVar, Generic, Callable, Any, Iterable

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

        modules.add(self)

        if self.serializer is not None:
            register_output_serializer(self.output, self.serializer)

    def run(self, base_input: Any, steps: Optional[tuple] = None) -> T:
        """
        A cached version of the analyze method. All calls to analyze should be done through this method.

        :param base_input: The user provided JSON input.
        :param steps: Any previous calculates in the dependency graph.
        :return: The result of the analyze method.
        """
        if self.output in cache:
            return cache[self.output]

        result = self.analyze(base_input, steps)
        cache[self.output] = result

        return result

    def analyze(self, base_input: Any, steps: Optional[tuple] = None) -> T:
        """
        Main analysis method. This method will be overridden by an E3 module and include any calculations to create the
        desired output.

        :param base_input: The user provided JSON input.
        :param steps: Any previous calculates in the dependency graph.
        :return: The result of the defined calculation.
        """
        pass


modules: set[E3AppConfig] = set()
moduleFunctions: dict[str, Callable[[Any], T]] = {}

cache = {}


def init():
    """
    Initialization function that stores modules in global variables.
    """
    global moduleFunctions

    outputs = {module.output: module for module in modules}
    moduleFunctions = {module.output: create_analysis_function(module, outputs) for module in modules}


def reset():
    global cache

    cache = {}


def create_analysis_function(module: E3AppConfig, outputs: dict[str, E3AppConfig]) -> Callable[[Any], T]:
    """
    Helper function that wraps analysis methods in case they require dependencies to be computed first.

    :param module: The current module to look at.
    :param outputs: A dictionary of output object pointing to their associated modules.
    :return: Either the normal module function if no dependencies are defined or a wrapped function that calls all
    required dependencies beforehand.
    """
    if module.depends_on is None:
        return module.run

    return lambda *args, **kwargs: resolve(module, outputs)(*args, **kwargs)


def resolve(module: E3AppConfig, outputs: dict[str, E3AppConfig]) -> Callable[[Any], tuple]:
    """
    Helper function that recursively resolves any dependencies in a module.

    :param module: The current module to look at.
    :param outputs: A dictionary of output object pointing to their associated modules.
    :return: A wrapped function which returns the result of an analysis method and a list of its inputs.
    """

    # If we have no dependencies, return the modules run method.
    if module.depends_on is None:
        return module.run

    # If there are dependencies, get a function that recursively calls them all.
    inner_functions = [resolve(outputs[dependency], outputs) for dependency in module.depends_on]

    # Creates a function which passes through all required arguments to dependency functions.
    def wrapped(*args, **kwargs):
        steps = tuple(inner(*args, **kwargs) for inner in inner_functions)
        return module.run(*args, steps=steps)

    return wrapped
