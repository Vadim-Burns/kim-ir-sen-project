import abc
import multiprocessing


class AbstractEndpoint(abc.ABC):

    @abc.abstractmethod
    def run(self):
        ...

    @abc.abstractmethod
    def get_name(self) -> str:
        ...


class EndpointManager:

    def __init__(self):
        self._endpoints = []
        self._endpoint_procs = []

    def run(self):
        multiprocessing.set_start_method('fork')
        for end in self._endpoints:
            print(f"Starting {end.get_name()} endpoint")
            pc = multiprocessing.Process(target=end.run)
            pc.start()
            self._endpoint_procs.append(pc)
            print(f"{end.get_name()} endpoint has been started")

    def stop(self):
        for pc in self._endpoint_procs:
            pc.terminate()

    def add_endpoint(self, endpoint: AbstractEndpoint):
        self._endpoints.append(endpoint)
