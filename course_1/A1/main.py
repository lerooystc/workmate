from typing import Self


class ObjList():
    def __init__(self, data) -> None:
         self.__next = None
         self.__prev = None
         self.__data = data

    def get_next(self) -> Self:
        return self.__next
    
    def set_next(self, obj):
        self.__next = obj
        
    def get_prev(self) -> Self:
        return self.__prev
    
    def set_prev(self, obj):
        self.__prev = obj
        
    def get_data(self) -> any:
        return self.__data
    
    def set_data(self, data):
        self.__data = data
        
    def __str__(self) -> str:
        return self.__data


class LinkedList():
    def __init__(self) -> None:
        self.head = None
        self.tail = None
    
    def add_obj(self, obj: ObjList) -> None:
        if not self.head:
            self.head = obj
            self.tail = obj
        else:
            prev = self.tail
            obj.set_prev(prev)
            prev.set_next(obj=obj)
            self.tail = obj
            
    def remove_obj(self) -> None:
        if self.tail:
            to_be_deleted = self.tail
            prev = to_be_deleted.get_prev()
            if prev:
                self.tail = prev
                to_be_deleted.set_prev(None)
                prev.set_next(None)
            else:
                self.tail = None
                self.head = None
            
    def get_data(self) -> list:
        res = []
        current = self.head
        while current:
            res.append(current.get_data())
            current = current.get_next()
        return res
        
    
lst = LinkedList()
lst.add_obj(ObjList("1"))
lst.remove_obj()
print(lst.get_data())