from unittest import TestCase

from aoc.data_structures.linked_list import LinkedListElement, LoopingUniqueLinkedList, UniqueLinkedList


class TestUniqueLinkedList(TestCase):
    def assert_list_equal(self, linked_list: UniqueLinkedList, expected: list):
        self.assertEqual(len(linked_list), len(expected),
                         f'expected length {len(expected)}, got length {len(linked_list)}')
        if not len(expected):
            self.assertIsNone(linked_list.first, 'expected empty list, has first element')
            self.assertIsNone(linked_list.last, 'expected empty list, has last element')
            return
        current = LinkedListElement(0, next_element=linked_list.first)
        for value in expected:
            current = current.next_element
            self.assertEqual(value, current.value, f'{expected} is not {list(linked_list)}')
        self.assertEqual(linked_list.first.value, expected[0],
                         f'expected first {expected[0]}, but is {linked_list.first.value}')
        self.assertEqual(linked_list.last.value, expected[-1],
                         f'expected last {expected[-1]}, but is {linked_list.last.value}')

    def test__get_element__by_element(self):
        linked_list = UniqueLinkedList([1])
        element = linked_list._get_element(linked_list.first)
        self.assertIsNotNone(element)
        self.assertEqual(element.value, 1)
        self.assertIs(element, linked_list.first)

    def test__get_element__by_value(self):
        linked_list = UniqueLinkedList([1])
        element = linked_list._get_element(1)
        self.assertIsNotNone(element)
        self.assertEqual(element.value, 1)
        self.assertIs(element, linked_list.first)

    def test__get_element__exceptions(self):
        linked_list = UniqueLinkedList([1])
        self.assertRaises(ValueError, linked_list._get_element, 2)
        self.assertRaises(ValueError, linked_list._get_element, LinkedListElement(1))
        self.assertRaises(ValueError, linked_list._get_element, LinkedListElement(2))

    def test__get_element__replace(self):
        linked_list = UniqueLinkedList([1])
        element = linked_list._get_element(LinkedListElement(1), replace=True)
        self.assertIsNotNone(element)
        self.assertEqual(element.value, 1)
        self.assertIs(element, linked_list.first)

    def test__add_element(self):
        linked_list = UniqueLinkedList()
        original = LinkedListElement(1)
        element = linked_list._add_element(original)
        self.assertEqual(element.value, 1)
        self.assertIsNot(element, original)

    def test__add_element__keep(self):
        original = LinkedListElement(1)
        linked_list = UniqueLinkedList()
        element = linked_list._add_element(original, keep_element=True)
        self.assertIs(element, original)

    def test__add_element__value(self):
        linked_list = UniqueLinkedList()
        element = linked_list._add_element(3)
        self.assertEqual(element.value, 3)
        linked_list = UniqueLinkedList()
        linked_list._add_element(4, keep_element=True)

    def test__add_element__exceptions(self):
        linked_list = UniqueLinkedList([1])
        self.assertRaises(ValueError, linked_list._add_element, 1)
        self.assertRaises(ValueError, linked_list._add_element, LinkedListElement(1))

    def test__add_elements(self):
        original1 = LinkedListElement(1)
        original2 = LinkedListElement(2)
        for originals in [
            (original1, original2),
            [original1, original2],
            iter([original1, original2]),
            UniqueLinkedList([original1, original2]),
            reversed([original2, original1])
        ]:
            linked_list = UniqueLinkedList()
            elements = linked_list._add_elements(originals)
            self.assertEqual(elements[1].value, original1.value)
            self.assertEqual(elements[2].value, original2.value)
            self.assertIsNot(elements[1], original1)
            self.assertIsNot(elements[2], original2)
            self.assertIs(elements[1], linked_list.elements[1])
            self.assertIs(elements[2], linked_list.elements[2])

    def test__add_elements__empty(self):
        linked_list = UniqueLinkedList()
        elements = linked_list._add_elements([])
        self.assertFalse(elements)
        self.assertFalse(linked_list.elements)

    def test__add_elements__keep(self):
        original1 = LinkedListElement(1)
        original2 = LinkedListElement(2)
        linked_list = UniqueLinkedList()
        elements = linked_list._add_elements([original1, original2], keep_elements=True)
        self.assertIs(elements[1], original1)
        self.assertIs(elements[2], original2)

    def test__add_elements__values(self):
        linked_list = UniqueLinkedList()
        elements = linked_list._add_elements([1, 2])
        self.assertEqual(elements[1].value, 1)
        self.assertEqual(elements[2].value, 2)
        linked_list = UniqueLinkedList()
        linked_list._add_elements([1, 2], keep_elements=True)

    def test__add_elements__exceptions(self):
        linked_list = UniqueLinkedList([1])
        self.assertRaises(ValueError, linked_list._add_elements, [1, 2])
        self.assertRaises(ValueError, linked_list._add_elements, [2, 2])
        self.assertRaises(ValueError, linked_list._add_elements, [LinkedListElement(1)])
        self.assertRaises(ValueError, linked_list._add_elements, [LinkedListElement(2), LinkedListElement(2)])
        self.assertRaises(ValueError, linked_list._add_elements, [LinkedListElement(2), 2])

    def test__add_elements__atomic(self):
        linked_list = UniqueLinkedList([1])
        self.assertRaises(ValueError, linked_list._add_elements, [2, 3, 4, 5, 2])
        self.assertEqual(len(linked_list.elements), 1)

    def test__check_correct_order(self):
        linked_list = UniqueLinkedList([1, 2])
        linked_list._check_correct_order(linked_list.first, linked_list.first)
        linked_list._check_correct_order(linked_list.first, linked_list.last)
        linked_list._check_correct_order(linked_list.last, linked_list.last)
        self.assertRaises(ValueError, linked_list._check_correct_order, linked_list.last, linked_list.first)

    def test_init__empty(self):
        self.assertIsNotNone(UniqueLinkedList())
        self.assertIsNotNone(UniqueLinkedList(None))
        self.assertIsNotNone(UniqueLinkedList([]))
        self.assertIsNotNone(UniqueLinkedList(UniqueLinkedList([])))

    def test_init__full(self):
        linked_list = UniqueLinkedList([1])
        self.assertEqual(len(linked_list.elements), 1)
        self.assertEqual(linked_list.first.value, 1)
        self.assertEqual(linked_list.last.value, 1)

        linked_list = UniqueLinkedList([LinkedListElement(1)])
        self.assertEqual(len(linked_list.elements), 1)
        self.assertEqual(linked_list.first.value, 1)
        self.assertEqual(linked_list.last.value, 1)

        linked_list = UniqueLinkedList([1, 2])
        self.assertEqual(len(linked_list.elements), 2)
        self.assertEqual(linked_list.first.value, 1)
        self.assertEqual(linked_list.last.value, 2)

        linked_list = UniqueLinkedList(range(5))
        self.assertEqual(len(linked_list.elements), 5)
        self.assertEqual(linked_list.first.value, 0)
        self.assertEqual(linked_list.last.value, 4)

        linked_list2 = UniqueLinkedList(linked_list)
        self.assertEqual(len(linked_list2.elements), 5)
        self.assertEqual(linked_list2.first.value, 0)
        self.assertEqual(linked_list2.last.value, 4)
        self.assertIsNot(linked_list.first, linked_list2.first)
        self.assertIsNot(linked_list.last, linked_list2.last)

    def test_get(self):
        linked_list = UniqueLinkedList([1, 2, 3])
        self.assertIs(linked_list.get(3), linked_list.last)
        self.assertIsNone(linked_list.get(4))

    def test_append(self):
        linked_list = UniqueLinkedList([1])
        linked_list.append(2)
        self.assertEqual(len(linked_list.elements), 2)
        self.assertEqual(linked_list.first.value, 1)
        self.assertEqual(linked_list.last.value, 2)

        linked_list = UniqueLinkedList([2, 3])
        linked_list.append(4)
        linked_list.append(1)
        self.assertEqual(len(linked_list.elements), 4)
        self.assertEqual(linked_list.first.value, 2)
        self.assertEqual(linked_list.last.value, 1)

    def test_append__exceptions(self):
        linked_list = UniqueLinkedList([1])
        self.assertRaises(ValueError, linked_list.append, 1)

    def test_prepend(self):
        linked_list = UniqueLinkedList([1])
        linked_list.prepend(2)
        self.assertEqual(len(linked_list.elements), 2)
        self.assertEqual(linked_list.first.value, 2)
        self.assertEqual(linked_list.last.value, 1)

        linked_list = UniqueLinkedList([2, 3])
        linked_list.prepend(4)
        linked_list.prepend(1)
        self.assertEqual(len(linked_list.elements), 4)
        self.assertEqual(linked_list.first.value, 1)
        self.assertEqual(linked_list.last.value, 3)

    def test_prepend__exceptions(self):
        linked_list = UniqueLinkedList([1])
        self.assertRaises(ValueError, linked_list.prepend, 1)

    def test_extend(self):
        linked_list = UniqueLinkedList()
        linked_list.extend([1, 2])
        linked_list.extend([3, 4])
        self.assertEqual(len(linked_list.elements), 4)
        self.assertEqual(linked_list.first.value, 1)
        self.assertEqual(linked_list.last.value, 4)
        linked_list2 = UniqueLinkedList([5, 6])
        linked_list.extend(linked_list2)
        self.assertEqual(linked_list.last.value, 6)
        self.assertIsNot(linked_list.last, linked_list2.last)

    def test_extend__keep(self):
        linked_list = UniqueLinkedList([1, 2])
        linked_list2 = UniqueLinkedList([3, 4])
        linked_list.extend(linked_list2, keep_elements=True)
        self.assertEqual(linked_list.last.value, 4)
        self.assertIs(linked_list.last, linked_list2.last)

    def test_pre_extend(self):
        linked_list = UniqueLinkedList()
        linked_list.pre_extend([1, 2])
        linked_list.pre_extend([3, 4])
        self.assertEqual(len(linked_list.elements), 4)
        self.assertEqual(linked_list.first.value, 3)
        self.assertEqual(linked_list.last.value, 2)
        linked_list2 = UniqueLinkedList([5, 6])
        linked_list.pre_extend(linked_list2)
        self.assertEqual(linked_list.first.value, 5)
        self.assertEqual(linked_list.last.value, 2)
        self.assertIsNot(linked_list.first, linked_list2.first)

    def test_pre_extend__keep(self):
        linked_list = UniqueLinkedList([1, 2])
        linked_list2 = UniqueLinkedList([3, 4])
        linked_list.pre_extend(linked_list2, keep_elements=True)
        self.assertEqual(linked_list.first.value, 3)
        self.assertIs(linked_list.first, linked_list2.first)

    def test_insert_before__element(self):
        linked_list = UniqueLinkedList([1, 2])
        original = LinkedListElement(3)
        element = linked_list.insert_before(linked_list.last, original)
        self.assert_list_equal(linked_list, [1, 3, 2])
        self.assertIsNot(element, original)
        self.assertIsNot(linked_list[1], original)

    def test_insert_before__first(self):
        linked_list = UniqueLinkedList([1, 2])
        linked_list.insert_before(linked_list.first, 3)
        self.assert_list_equal(linked_list, [3, 1, 2])

    def test_insert_before__value(self):
        linked_list = UniqueLinkedList([1, 2])
        linked_list.insert_before(2, 3)
        self.assert_list_equal(linked_list, [1, 3, 2])

    def test_insert_before__keep(self):
        linked_list = UniqueLinkedList([1, 2])
        original = LinkedListElement(3)
        element = linked_list.insert_before(2, original, keep_element=True)
        self.assert_list_equal(linked_list, [1, 3, 2])
        self.assertIs(element, original)
        self.assertIs(linked_list.first.next_element, original)

    def test_insert_before_index(self):
        linked_list = UniqueLinkedList([1, 2])
        original = LinkedListElement(3)
        element = linked_list.insert_before_index(1, original)
        self.assert_list_equal(linked_list, [1, 3, 2])
        self.assertIsNot(element, original)
        self.assertIsNot(linked_list[1], original)

    def test_insert_before_index__keep(self):
        linked_list = UniqueLinkedList([1, 2])
        original = LinkedListElement(3)
        element = linked_list.insert_before_index(1, original, keep_element=True)
        self.assert_list_equal(linked_list, [1, 3, 2])
        self.assertIs(element, original)
        self.assertIs(linked_list.first.next_element, original)

    def test_insert_after__element(self):
        linked_list = UniqueLinkedList([1, 2])
        original = LinkedListElement(3)
        element = linked_list.insert_after(linked_list.first, original)
        self.assert_list_equal(linked_list, [1, 3, 2])
        self.assertIsNot(element, original)
        self.assertIsNot(linked_list[1], original)

    def test_insert_after__last(self):
        linked_list = UniqueLinkedList([1, 2])
        linked_list.insert_after(linked_list.last, 3)
        self.assert_list_equal(linked_list, [1, 2, 3])

    def test_insert_after__value(self):
        linked_list = UniqueLinkedList([1, 2])
        linked_list.insert_after(1, 3)
        self.assert_list_equal(linked_list, [1, 3, 2])

    def test_insert_after__keep(self):
        linked_list = UniqueLinkedList([1, 2])
        original = LinkedListElement(3)
        element = linked_list.insert_after(1, original, keep_element=True)
        self.assert_list_equal(linked_list, [1, 3, 2])
        self.assertIs(element, original)
        self.assertIs(linked_list.first.next_element, original)

    def test_insert_after_index(self):
        linked_list = UniqueLinkedList([1, 2])
        original = LinkedListElement(3)
        element = linked_list.insert_after_index(0, original)
        self.assert_list_equal(linked_list, [1, 3, 2])
        self.assertIsNot(element, original)
        self.assertIsNot(linked_list[1], original)

    def test_insert_after_index__keep(self):
        linked_list = UniqueLinkedList([1, 2])
        original = LinkedListElement(3)
        element = linked_list.insert_after_index(0, original, keep_element=True)
        self.assert_list_equal(linked_list, [1, 3, 2])
        self.assertIs(element, original)
        self.assertIs(linked_list.first.next_element, original)

    def test_remove(self):
        linked_list = UniqueLinkedList([1, 2, 3])
        linked_list.remove(linked_list.first)
        self.assert_list_equal(linked_list, [2, 3])
        linked_list.remove(linked_list.last)
        self.assert_list_equal(linked_list, [2])
        linked_list = UniqueLinkedList([1, 2, 3])
        linked_list.remove(2)
        self.assert_list_equal(linked_list, [1, 3])
        compare = linked_list.first
        self.assertIs(linked_list.remove(1), compare)

    def test_extract__by_element(self):
        linked_list = UniqueLinkedList(reversed(range(5)))
        new_list = linked_list.extract(linked_list.first.next_element, linked_list.last.previous_element)
        self.assert_list_equal(linked_list, [4, 0])
        self.assert_list_equal(new_list, [3, 2, 1])

    def test_extract__by_value(self):
        linked_list = UniqueLinkedList(reversed(range(5)))
        new_list = linked_list.extract(3, 1)
        self.assert_list_equal(linked_list, [4, 0])
        self.assert_list_equal(new_list, [3, 2, 1])

    def test_extract__all(self):
        linked_list = UniqueLinkedList(reversed(range(5)))
        new_list = linked_list.extract(linked_list.first, linked_list.last)
        self.assert_list_equal(linked_list, [])
        self.assert_list_equal(new_list, [4, 3, 2, 1, 0])

    def test_extract_from(self):
        linked_list = UniqueLinkedList(reversed(range(5)))
        new_list = linked_list.extract_from(3, 3)
        self.assert_list_equal(linked_list, [4, 0])
        self.assert_list_equal(new_list, [3, 2, 1])

    def test_extract_from__exceptions(self):
        linked_list = UniqueLinkedList(reversed(range(5)))
        self.assertRaises(ValueError, linked_list.extract_from, 1, 3)

    def test_extract_index(self):
        linked_list = UniqueLinkedList(reversed(range(5)))
        new_list = linked_list.extract_index(1, 3)
        self.assert_list_equal(linked_list, [4, 0])
        self.assert_list_equal(new_list, [3, 2, 1])

    def test_extract_from_index(self):
        linked_list = UniqueLinkedList(reversed(range(5)))
        new_list = linked_list.extract_from_index(1, 2)
        self.assert_list_equal(linked_list, [4, 1, 0])
        self.assert_list_equal(new_list, [3, 2])

    def test_clear(self):
        linked_list = UniqueLinkedList(range(5))
        linked_list.clear()
        self.assert_list_equal(linked_list, [])
        self.assertFalse(linked_list.elements)

    def test_sort(self):
        linked_list = UniqueLinkedList(reversed(range(5)))
        linked_list.sort()
        self.assert_list_equal(linked_list, [0, 1, 2, 3, 4])

    def test_reverse(self):
        linked_list = UniqueLinkedList(range(5))
        linked_list.reverse()
        self.assert_list_equal(linked_list, [4, 3, 2, 1, 0])

    def test_copy(self):
        linked_list = UniqueLinkedList(range(5))
        copy = linked_list.copy()
        self.assert_list_equal(copy, list(range(5)))
        for i in range(5):
            self.assertIsNot(copy[i], linked_list[i])

    def test__iterators(self):
        linked_list = UniqueLinkedList(range(5))
        self.assert_list_equal(linked_list, list(element.value for element in linked_list))
        reversed_list = UniqueLinkedList(reversed(range(5)))
        self.assert_list_equal(reversed_list, list(element.value for element in reversed(linked_list)))

    def test__getitem(self):
        linked_list = UniqueLinkedList(range(5))
        for i in range(5):
            self.assertEqual(linked_list[i].value, i)
        for i in range(-1, -6, -1):
            self.assertEqual(linked_list[i].value, 5 + i)
        self.assertRaises(TypeError, linked_list.__getitem__, 'q')
        self.assertRaises(IndexError, linked_list.__getitem__, 5)
        self.assertRaises(IndexError, linked_list.__getitem__, -6)


class TestLoopingUniqueLinkedList(TestUniqueLinkedList):
    def assert_looping(self, linked_list: LoopingUniqueLinkedList):
        if linked_list.first is not None:
            self.assertIs(linked_list.first.previous_element, linked_list.last, 'list is not looping')
            self.assertIs(linked_list.last.next_element, linked_list.first, 'list is not looping')

    def test_init(self):
        linked_list = LoopingUniqueLinkedList([1, 2, 3])
        self.assert_looping(linked_list)

    def test_append(self):
        linked_list = LoopingUniqueLinkedList([1])
        linked_list.append(2)
        self.assert_looping(linked_list)

    def test_prepend(self):
        linked_list = LoopingUniqueLinkedList([1])
        linked_list.prepend(2)
        self.assert_looping(linked_list)

    def test_extend(self):
        linked_list = LoopingUniqueLinkedList([1, 2])
        linked_list.extend([3, 4])
        self.assert_looping(linked_list)

    def test_extend__keep(self):
        linked_list = LoopingUniqueLinkedList([1, 2])
        linked_list.extend([3, 4], keep_elements=True)
        self.assert_looping(linked_list)

    def test_pre_extend(self):
        linked_list = LoopingUniqueLinkedList([1, 2])
        linked_list.pre_extend([3, 4])
        self.assert_looping(linked_list)

    def test_pre_extend__keep(self):
        linked_list = LoopingUniqueLinkedList([1, 2])
        linked_list.pre_extend([3, 4], keep_elements=True)
        self.assert_looping(linked_list)

    def test_insert_before__first(self):
        linked_list = LoopingUniqueLinkedList([1, 2])
        linked_list.insert_before(linked_list.first, 3)
        self.assert_looping(linked_list)

    def test_insert_before__keep(self):
        linked_list = LoopingUniqueLinkedList([1, 2])
        linked_list.insert_before(1, LinkedListElement(3), keep_element=True)
        self.assert_looping(linked_list)

    def test_insert_before_index(self):
        linked_list = LoopingUniqueLinkedList([1, 2])
        linked_list.insert_before_index(0, 3)
        self.assert_looping(linked_list)

    def test_insert_after__last(self):
        linked_list = LoopingUniqueLinkedList([1, 2])
        linked_list.insert_after(linked_list.last, 3)
        self.assert_looping(linked_list)

    def test_insert_after__keep(self):
        linked_list = LoopingUniqueLinkedList([1, 2])
        linked_list.insert_after(1, 3, keep_element=True)
        self.assert_looping(linked_list)

    def test_insert_after_index(self):
        linked_list = LoopingUniqueLinkedList([1, 2])
        linked_list.insert_after_index(0, 3)
        self.assert_looping(linked_list)

    def test_insert_after_index__keep(self):
        linked_list = LoopingUniqueLinkedList([1, 2])
        linked_list.insert_after_index(0, 3, keep_element=True)
        self.assert_looping(linked_list)

    def test_remove(self):
        linked_list = LoopingUniqueLinkedList([1, 2, 3])
        linked_list.remove(linked_list.first)
        self.assert_looping(linked_list)
        linked_list.remove(linked_list.last)
        self.assert_looping(linked_list)

    def test_extract(self):
        linked_list = LoopingUniqueLinkedList(reversed(range(5)))
        new_list = linked_list.extract(1, 4)
        self.assert_looping(linked_list)
        self.assert_list_equal(linked_list, [3, 2])
        self.assert_list_equal(new_list, [1, 0, 4])

    def test_extract_from(self):
        linked_list = LoopingUniqueLinkedList(reversed(range(5)))
        new_list = linked_list.extract_from(0, 3)
        self.assert_looping(linked_list)
        self.assert_list_equal(linked_list, [2, 1])
        self.assert_list_equal(new_list, [0, 4, 3])

    def test_extract_index(self):
        linked_list = LoopingUniqueLinkedList(reversed(range(5)))
        new_list = linked_list.extract_index(4, 1)
        self.assert_list_equal(linked_list, [2, 1])
        self.assert_list_equal(new_list, [0, 4, 3])

    def test_extract_from_index(self):
        linked_list = LoopingUniqueLinkedList(reversed(range(5)))
        new_list = linked_list.extract_from_index(4, 3)
        self.assert_list_equal(linked_list, [2, 1])
        self.assert_list_equal(new_list, [0, 4, 3])

    def test_sort(self):
        linked_list = LoopingUniqueLinkedList(reversed(range(5)))
        linked_list.sort()
        self.assert_list_equal(linked_list, [0, 1, 2, 3, 4])
        self.assert_looping(linked_list)

    def test_reverse(self):
        linked_list = LoopingUniqueLinkedList(range(5))
        linked_list.reverse()
        self.assert_list_equal(linked_list, [4, 3, 2, 1, 0])
        self.assert_looping(linked_list)

    def test_copy(self):
        linked_list = LoopingUniqueLinkedList(range(5))
        copy = linked_list.copy()
        self.assert_list_equal(copy, list(range(5)))
        for i in range(5):
            self.assertIsNot(copy[i], linked_list[i])
        self.assert_looping(linked_list)

    def test__iterators(self):
        linked_list = LoopingUniqueLinkedList(range(5))
        self.assert_list_equal(linked_list, list(element.value for element in linked_list))
        reversed_list = LoopingUniqueLinkedList(reversed(range(5)))
        self.assert_list_equal(reversed_list, list(element.value for element in reversed(linked_list)))

    def test__getitem(self):
        linked_list = LoopingUniqueLinkedList(range(5))
        for i in range(10):
            self.assertEqual(linked_list[i].value, i % 5)
        for i in range(-1, -11, -1):
            self.assertEqual(linked_list[i].value, (5 + i) % 5)
        self.assertRaises(TypeError, linked_list.__getitem__, 'q')
