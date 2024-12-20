from dataclasses import dataclass
from itertools import count as it_count
from typing import Self

# я бы это все переписал (как минимум в data добавил бы ip отправившего?)


@dataclass
class Data:
    data: str
    ip_dest: int


class Server:
    id_server = it_count(1)

    def __init__(self) -> None:
        self.buffer: dict[Self, Data] = dict()
        self.ip: int = next(Server.id_server)
        self.router: Router = None

    def get_ip(self) -> int:
        """Получение ip-адреса сервера"""
        return self.ip

    def send_data(self, data: Data) -> None:
        """Отправление данных на роутер"""
        self.router.add_to_buffer(data, self)

    def get_data(self) -> dict[Self, Data]:
        """Получение и очищение буффера"""
        buffer = self.buffer
        self.buffer = dict()
        return buffer

    def add_to_buffer(self, data: Data, server: Self) -> None:
        """Добавление в буфер"""
        self.buffer.setdefault(server, []).append(data)

    def set_router(self, router: "Router"):
        """Сеттер для роутера"""
        self.router = router

    def __hash__(self) -> int:
        """Хэшинг для назначения сервера ключом словаря"""
        return hash(self.ip)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Server):
            return self.ip == __value.ip
        return NotImplemented

    def __repr__(self) -> str:
        return str(self.ip)


class Router:
    def __init__(self) -> None:
        self.buffer: dict[Server, Data] = dict()
        self.servers: dict[int, Server] = dict()

    def link(self, server: Server) -> None:
        """Линкинг"""
        self.servers[server.get_ip()] = server
        server.set_router(self)

    def unlink(self, server: Server) -> None:
        """Делинкинг"""
        del self.servers[server.get_ip()]
        server.set_router(None)

    def send_data(self) -> None:
        """Отправление в буфферы всем серверам"""
        for server, data in self.buffer.items():
            for message in data:
                message: Data
                receiver = self.servers.get(message.ip_dest)
                if receiver:
                    receiver.add_to_buffer(message, server)
        self.buffer = dict()

    def add_to_buffer(self, data: Data, server: Server) -> None:
        """Добавление в буфер"""
        self.buffer.setdefault(server, []).append(data)


router = Router()
sv_from = Server()
sv_from2 = Server()
router.link(sv_from)
router.link(sv_from2)
router.link(Server())
router.link(Server())
sv_to = Server()
router.link(sv_to)
sv_from.send_data(Data("Hello", sv_to.get_ip()))
sv_from.send_data(Data("Hello", sv_to.get_ip()))
sv_from2.send_data(Data("Hello2", sv_to.get_ip()))
sv_to.send_data(Data("Hi", sv_from.get_ip()))
router.send_data()
msg_list_from = sv_from.get_data()
msg_list_to = sv_to.get_data()
print(msg_list_from)
print(msg_list_to)
sv_from2.send_data(Data("Hi from from2 to from1", sv_from.get_ip()))
router.send_data()
msg_list_from = sv_from.get_data()
print(msg_list_from)
