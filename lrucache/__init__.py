# -*- coding: utf-8 -*-
from lrucache.linkedlist import LinkedList, LinkedListNode


class CacheMissException(Exception):
    def __init__(self, missing_key):
        self.missing_key = missing_key

    def __str__(self):
        return 'Cache miss for key: {0}'.format(self.missing_key)


class LRUCache(object):
    def __init__(self, size):
        if size < 1:
            raise ValueException('Value for cache size should be positive, '
                                 'provided: {0}'.format(size))
        self.size = size
        self.value_map = {}
        self.recents = LinkedList()

    def get(self, key):
        try:
            node, value = self.value_map[key]
            self.recents.remove_node(node)
            self.recents.push_front(node)
            return value
        except KeyError as k:
            raise CacheMissException(key)

    def put(self, key, value):
        try:
            node, old_value = self.value_map[key]
            self.recents.remove_node(node)
        except KeyError as k:  # not in map
            if len(self.recents) >= self.size:
                back_node = self.recents.pop_back()
                del self.value_map[back_node.data]
            node = LinkedListNode(key)
        self.recents.push_front(node)
        self.value_map[key] = node, value
