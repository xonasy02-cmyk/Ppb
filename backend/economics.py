"""Private accounting primitives. No trading or settlement without a configured protocol.

Values are SOL-denominated Decimal, not reward-asset market quotes.
These functions are not exposed as public fee metadata or mutation endpoints.
"""
from decimal import Decimal

def split_creator_fee(amount: Decimal):
    if not amount.is_finite() or amount < 0:
        raise ValueError('Fee must be non-negative and finite')
    creator = amount * Decimal('0.4')
    bag = amount * Decimal('0.4')
    return {'creator':creator,'bag':bag,'global':amount-creator-bag}

def native_settlement(amount: Decimal):
    if not amount.is_finite() or amount < 0:
        raise ValueError('Bag value must be non-negative and finite')
    share = amount * Decimal('0.8')
    return {'share':share,'buyback_burn':amount-share}

def eligible_carry_profit(realized_pnl: Decimal, settled: bool):
    if not realized_pnl.is_finite():
        raise ValueError('P&L must be finite')
    return max(realized_pnl, Decimal('0')) if settled else Decimal('0')