# -*- coding: utf-8 -*-

import pytest

from clive.validate import (
    BoolT,
    DateT,
    DictOfT,
    IntT,
    ListOfT,
    Result,
    T,
    TextT,
    validate_item,
)


class TestT:
    def test_required_with_none(self):
        assert (
            T(required=True).validate(None, '') ==
            [Result(0, 0, '', 'value required')]
        )

    @pytest.mark.parametrize('test_input', [
        True,
        False,
        0,
        [],
        {},
    ])
    def test_required_not_none(self, test_input):
        assert T(required=True).validate(test_input, '') == []

    @pytest.mark.parametrize('test_input', [
        None,
        True,
        False,
        0,
        [],
        {},
    ])
    def test_not_required(self, test_input):
        """Test not_required=True accepts all values including None"""
        assert T(required=False).validate(test_input, '') == []


class TestIntT:
    def test_required(self):
        assert (
            IntT(required=True).validate(None, '') ==
            [Result(0, 0, '', 'value required')]
        )
        assert IntT(required=True).validate(0, '') == []
        assert IntT(required=True).validate(1, '') == []

    def test_int(self):
        assert IntT().validate(1, '') == []
        assert IntT().validate(-1, '') == []

    @pytest.mark.parametrize('test_input', [
        True,
        False,
        'foo',
    ])
    def test_non_int(self, test_input):
        assert (
            IntT().validate(test_input, '') ==
            [Result(0, 0, '', 'value is not a valid int: %r' % test_input)]
        )


class TestBoolT:
    def test_required(self):
        assert (
            BoolT(required=True).validate(None, '') ==
            [Result(0, 0, '', 'value required')]
        )
        assert BoolT(required=True).validate(True, '') == []
        assert BoolT(required=True).validate(False, '') == []

    def test_bool(self):
        assert BoolT().validate(True, '') == []
        assert BoolT().validate(False, '') == []

    @pytest.mark.parametrize('test_input', [
        0,
        1,
        'foo'
    ])
    def test_non_bool(self, test_input):
        assert (
            BoolT().validate(test_input, '') ==
            [Result(0, 0, '', 'value is not a valid bool: %r' % test_input)]
        )


class TestTextT:
    def test_required(self):
        assert (
            TextT(required=True).validate(None, '') ==
            [Result(0, 0, '', 'value required')]
        )
        assert TextT(required=True).validate('', '') == []
        assert TextT(required=True).validate('foo', '') == []

    def test_text(self):
        assert TextT().validate('', '') == []
        assert TextT().validate('foo', '') == []

    def test_non_text(self):
        assert (
            TextT().validate(0, '') ==
            [Result(0, 0, '', 'value is not a valid text value: 0')]
        )

    @pytest.mark.parametrize('test_input', [
        'foo',
        'foo-bar',
        'foo_bar',
    ])
    def test_slug(self, test_input):
        assert TextT(slug=True).validate(test_input, '') == []

    @pytest.mark.parametrize('test_input', [
        '',
        'foo.bar',
        # FIXME: more variations here
    ])
    def test_non_slug(self, test_input):
        assert (
            TextT(slug=True).validate(test_input, '') ==
            [Result(0, 0, '', 'value is not a valid slug: %r' % test_input)]
        )


class TestDateT:
    def test_required(self):
        assert (
            DateT(required=True).validate(None, '') ==
            [Result(0, 0, '', 'value required')]
        )
        assert DateT(required=True).validate('2016-02-14', '') == []

    def test_date(self):
        assert DateT(required=True).validate('2016-02-14', '') == []

    @pytest.mark.parametrize('test_input', [
        '',
        '2005',
        '2005-12',
        '20051214',
    ])
    def test_non_date(self, test_input):
        assert (
            DateT(required=True).validate(test_input, '') ==
            [Result(0, 0, '', 'value is not date in YYYY-MM-DD format: %r' % test_input)]
        )


class TestListOfT:
    def test_required(self):
        assert (
            ListOfT(IntT(), required=True).validate(None, '') ==
            [Result(0, 0, '', 'value required')]
        )
        assert ListOfT(IntT(), required=True).validate([], '') == []

    def test_subtype(self):
        assert ListOfT(IntT()).validate([], '') == []
        assert ListOfT(IntT()).validate([1], '') == []
        assert ListOfT(TextT()).validate(['foo', 'bar'], '') == []

    def test_bad_subtype(self):
        assert (
            ListOfT(IntT()).validate(['foo'], '') ==
            [Result(0, 0, '[0]', 'value is not a valid int: %r' % 'foo')]
        )
        assert (
            ListOfT(IntT()).validate([10, 'foo'], '') ==
            [Result(0, 0, '[1]', 'value is not a valid int: %r' % 'foo')]
        )

    def test_depth(self):
        assert (
            ListOfT(IntT()).validate([10, 'foo'], 'TOP') ==
            [Result(0, 0, 'TOP[1]', 'value is not a valid int: %r' % 'foo')]
        )

    def test_recursion(self):
        assert ListOfT(ListOfT(IntT())).validate([[10, 2], [1, 2, 3]], 'TOP') == []
        assert (
            ListOfT(ListOfT(IntT())).validate([[10, 2], [1, 'foo', 3]], 'TOP') ==
            [Result(0, 0, 'TOP[1][1]', 'value is not a valid int: %r' % 'foo')]
        )
        assert (
            ListOfT(ListOfT(IntT())).validate([[10, 2], [1, 'foo', 'bar', 3]], 'TOP') ==
            [
                Result(0, 0, 'TOP[1][1]', 'value is not a valid int: %r' % 'foo'),
                Result(0, 0, 'TOP[1][2]', 'value is not a valid int: %r' % 'bar'),
            ]
        )


class TestDictOfT:
    def test_required(self):
        assert (
            DictOfT({'foo': IntT()}, required=True).validate(None, '') ==
            [Result(0, 0, '', 'value required')]
        )
        assert DictOfT({'foo': IntT()}, required=True).validate({}, '') == []

    def test_bad_value(self):
        assert (
            DictOfT({'foo': IntT()}).validate(5, '') ==
            [Result(0, 0, '', 'value is not a dict: %r' % 5)]
        )

    def test_subtype(self):
        assert DictOfT({'foo': IntT()}).validate({'foo': 5}, '') == []
        assert DictOfT({'foo': TextT()}).validate({'foo': 'bar'}, '') == []
        assert DictOfT({'foo': TextT(), 'bar': IntT()}).validate({'foo': 'val1', 'bar': 5}, '') == []

    def test_bad_subtype(self):
        assert (
            DictOfT({'foo': IntT()}).validate({'foo': 'bar'}, '') ==
            [Result(0, 0, ':foo', 'value is not a valid int: %r' % 'bar')]
        )

    def test_unknown_keys(self):
        assert (
            DictOfT({'foo': IntT()}).validate({'bar': 5}, '') ==
            [Result(0, 0, '', 'unknown key: %r' % 'bar')]
        )

    def test_depth(self):
        assert (
            DictOfT({'foo': IntT()}).validate({'foo': 'bar'}, 'TOP') ==
            [Result(0, 0, 'TOP:foo', 'value is not a valid int: %r' % 'bar')]
        )

    def test_recursion(self):
        assert DictOfT({'foo': DictOfT({'bar': IntT()})}).validate({'foo': {'bar': 5}}, 'TOP') == []
        assert (
            DictOfT({'foo': DictOfT({'bar': IntT()})}).validate({'foo': {'bar': 'baz'}}, 'TOP') ==
            [Result(0, 0, 'TOP:foo:bar', 'value is not a valid int: %r' % 'baz')]
        )
        # This is kind of gross to look at--sorry.
        assert (
            DictOfT({
                'foo': IntT(),
                'bar': IntT(),
                'baz': DictOfT({
                    'key': IntT(),
                })
            }).validate({
                'foo': 5,
                'bar': 'foo1',
                'baz': {
                    'key': 'foo2'
                }
            }, 'TOP') ==
            [
                Result(0, 0, 'TOP:bar', 'value is not a valid int: %r' % 'foo1'),
                Result(0, 0, 'TOP:baz:key', 'value is not a valid int: %r' % 'foo2'),
            ]
        )
