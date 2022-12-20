import abc


class AbstractRepo(abc.ABC):
    entity = None

    def get_entity(self) -> type:
        return self.entity

    @abc.abstractmethod
    def save_instances(
            self,
            instances: list,
            **params
    ) -> list:
        ...

    @abc.abstractmethod
    def list(
            self,
            page: int = 0,
            limit: int = 0,
            **params
    ):
        ...

    @abc.abstractmethod
    def get(
            self,
            **params
    ) -> entity:
        ...

    @abc.abstractmethod
    def exists(
            self,
            **params
    ) -> bool:
        ...

    @abc.abstractmethod
    def count(
            self,
            **params
    ) -> int:
        ...

    @abc.abstractmethod
    def update(
            self,
            pk_key,
            **params
    ) -> None:
        ...

    @abc.abstractmethod
    def delete(
            self,
            id: int,
            **params
    ) -> None:
        ...


class AbstractNoteRepo(AbstractRepo):
    ...
