from functools import lru_cache
from typing import Optional, TypeVar, Generic, Callable, Any, Union

from django.apps import AppConfig

T = TypeVar('T')


class E3AppConfig(AppConfig, Generic[T]):
    """
    Sets configuration options for an E# module. This includes the name, its optional dependency, and the ID of what
    this module outputs.
    """
    name: str = ""
    depends_on: Optional[str] = None
    output: str = ""

    def __init__(self, app_name, app_module):
        """
        Registers this module with the registry. Raises an AssertionError if output is not defined.
        """
        super().__init__(app_name, app_module)

        if not self.output:
            raise AssertionError(f"E3 Module must define an output, value was {self.output}")

        modules.add(self)

    @lru_cache
    def run(self, baseInput: Any, steps: Optional[tuple] = None) -> T:
        """
        A cached version of the analyze method. All calls to analyze should be done through this method.

        :param baseInput: The user provided JSON input.
        :param steps: Any previous calculates in the dependency graph.
        :return: The result of the analyze method.
        """
        return self.analyze(baseInput, steps)

    def analyze(self, baseInput: Any, steps: Optional[tuple] = None) -> T:
        """
        Main analysis method. This method will be overridden by an E3 module and include any calculations to create the
        desired output.

        :param baseInput: The user provided JSON input.
        :param steps: Any previous calculates in the dependency graph.
        :return: The result of the defined calculation.
        """
        pass


modules: set[E3AppConfig] = set()
moduleFunctions: dict[str, Callable[[Any], T]] = {}


def init():
    """
    Initialization function that stores modules in global variables.
    """
    global moduleFunctions

    outputs = {module.output: module for module in modules}
    moduleFunctions = {module.output: createAnalysisFunction(module, outputs) for module in modules}

    for function in moduleFunctions.values():
        function(10)


def createAnalysisFunction(module: E3AppConfig, outputs: dict[str, E3AppConfig]) -> Callable[[Any], T]:
    """
    Helper function that wraps analysis methods in case they require dependencies to be computed first.

    :param module: The current module to look at.
    :param outputs: A dictionary of output object pointing to their associated modules.
    :return: Either the normal module function if no dependencies are defined or a wrapped function that calls all
    required dependencies beforehand.
    """
    if module.depends_on is None:
        return module.run

    return lambda *args, **kwargs: resolve(module, outputs)(*args, **kwargs)[0]


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
    inner = resolve(outputs[module.depends_on], outputs)

    # Creates a function which passes through all required arguments to dependency functions.
    def wrapped(*args, **kwargs):
        steps = inner(*args, **kwargs)
        if not isinstance(steps, tuple):
            steps = (steps,)

        return module.run(*args, steps=steps), *steps

    return wrapped
