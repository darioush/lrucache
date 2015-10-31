# -*- encoding: utf-8 -*-
import pytest

from lrucache import LRUCache, CacheMissException


def test_insert_one():
    cache = LRUCache(3)
    cache.put('key', 'val')
    assert cache.get('key') == 'val'


def test_update_one():
    cache = LRUCache(3)
    cache.put('key', 'val')
    cache.put('key', 'new val')
    assert cache.get('key') == 'new val'


def test_insert_many():
    cache = LRUCache(3)
    cache.put('key', 'val')
    cache.put('key2', 'val2')
    cache.put('key3', 'val3')
    assert cache.get('key3') == 'val3'


def test_insert_over_capacity():
    cache = LRUCache(3)
    cache.put('key1', 'val1')
    cache.put('key2', 'val2')
    cache.put('key3', 'val3')
    cache.put('key4', 'val4')

    with pytest.raises(CacheMissException) as ex:
        cache.get('key1')
        assert 'key1' in str(ex)
    assert cache.get('key2') == 'val2'
    assert cache.get('key3') == 'val3'
    assert cache.get('key4') == 'val4'


def test_insert_over_capacity_with_access():
    cache = LRUCache(3)
    cache.put('key1', 'val1')
    cache.put('key2', 'val2')
    cache.put('key3', 'val3')
    assert cache.get('key1') == 'val1'
    cache.put('key4', 'val4')

    with pytest.raises(CacheMissException) as ex:
        cache.get('key2')
        assert 'key2' in str(ex)
    assert cache.get('key1') == 'val1'
    assert cache.get('key3') == 'val3'
    assert cache.get('key4') == 'val4'


def test_insert_over_capacity_with_update():
    cache = LRUCache(3)
    cache.put('key1', 'val1')
    cache.put('key2', 'val2')
    cache.put('key3', 'val3')
    cache.put('key1', 'new val')
    assert cache.get('key1') == 'new val'
    cache.put('key4', 'val4')

    with pytest.raises(CacheMissException) as ex:
        cache.get('key2')
        assert 'key2' in str(ex)
    assert cache.get('key1') == 'new val'
    assert cache.get('key3') == 'val3'
    assert cache.get('key4') == 'val4'


def test_bad_capacity():
    with pytest.raises(Exception):
        LRUCache(0)
