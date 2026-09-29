"""Decimal economics checks: creator split, native 80/20, and carry eligibility guards."""

from decimal import Decimal

import pytest

from economics import eligible_carry_profit, native_settlement, split_creator_fee


def test_split_creator_fee_conserves_amount():
    amount = Decimal('5.75')
    split = split_creator_fee(amount)
    assert split['creator'] + split['bag'] + split['global'] == amount


def test_split_creator_fee_rejects_negative_and_nonfinite():
    with pytest.raises(ValueError):
        split_creator_fee(Decimal('-0.1'))
    with pytest.raises(ValueError):
        split_creator_fee(Decimal('NaN'))


def test_native_settlement_uses_fixed_80_20_and_conserves_amount():
    amount = Decimal('123.456')
    split = native_settlement(amount)
    assert split['share'] == amount * Decimal('0.8') and split['buyback_burn'] == amount - split['share']


def test_native_settlement_rejects_invalid_values():
    with pytest.raises(ValueError):
        native_settlement(Decimal('-1'))
    with pytest.raises(ValueError):
        native_settlement(Decimal('Infinity'))


def test_eligible_carry_profit_only_adds_realized_positive_profit():
    assert eligible_carry_profit(Decimal('2.25'), settled=True) == Decimal('2.25')
    assert eligible_carry_profit(Decimal('-9.4'), settled=True) == Decimal('0')
    assert eligible_carry_profit(Decimal('3.0'), settled=False) == Decimal('0')


def test_eligible_carry_profit_rejects_nonfinite():
    with pytest.raises(ValueError):
        eligible_carry_profit(Decimal('NaN'), settled=True)
