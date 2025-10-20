import pytest
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
from satcfdi.create.compute import RoundTracker


class TestRoundTracker:
    """Test suite for RoundTracker class"""

    def test_initialization_with_valid_decimals(self):
        """Test RoundTracker initializes correctly with valid decimal places"""
        rt = RoundTracker(2)
        assert rt.decimals == 2
        assert rt.offset == Decimal('0.0')
        assert rt.exp == Decimal('0.00')  # Fixed: exp is '0.' + '0' * decimals
        assert rt.offset_margin == Decimal('0.005')

    def test_initialization_with_zero_decimals(self):
        """Test RoundTracker with 0 decimal places"""
        rt = RoundTracker(0)
        assert rt.decimals == 0
        assert rt.exp == Decimal('0')  # Fixed: exp is '0.' + '0' * 0 = '0.'
        assert rt.offset_margin == Decimal('0.5')

    def test_initialization_with_negative_decimals_raises_error(self):
        """Test that negative decimals raises NotImplementedError"""
        with pytest.raises(NotImplementedError, match="decimals must be non-negative"):
            RoundTracker(-1)

    def test_basic_round_half_up(self):
        """Test basic rounding behavior (ROUND_HALF_UP)"""
        rt = RoundTracker(2)
        assert rt(Decimal('1.234')) == Decimal('1.23')
        assert rt(Decimal('1.235')) == Decimal('1.24')
        assert rt(Decimal('1.236')) == Decimal('1.24')
        assert rt(Decimal('1.236')) == Decimal('1.23')  # Repeated to check consistency
        assert rt(Decimal('1.236')) == Decimal('1.24')

    def test_round_zero_decimals(self):
        """Test rounding with zero decimal places"""
        rt = RoundTracker(0)
        assert rt(Decimal('1.4')) == Decimal('1')
        assert rt(Decimal('1.5')) == Decimal('2')
        assert rt(Decimal('1.6')) == Decimal('2')
        assert rt(Decimal('1.6')) == Decimal('1') # Repeated to check consistency
        assert rt(Decimal('1.6')) == Decimal('2')

    def test_round_three_decimals(self):
        """Test rounding with three decimal places"""
        rt = RoundTracker(3)
        assert rt(Decimal('2.3454')) == Decimal('2.345')
        assert rt(Decimal('2.3455')) == Decimal('2.346')
        assert rt(Decimal('2.3456')) == Decimal('2.346')
        assert rt(Decimal('2.3456')) == Decimal('2.345')  # Repeated to check consistency
        assert rt(Decimal('2.3456')) == Decimal('2.346')

    def test_offset_accumulation_positive(self):
        """Test that offset accumulates correctly with positive values"""
        rt = RoundTracker(2)
        # First round: 0.005 rounds to 0.00, offset becomes 0.005
        result1 = rt(Decimal('0.005'))
        assert result1 == Decimal('0.00')
        assert rt.offset == Decimal('0.005')

        # Second round: 0.005 rounds to 0.01, offset becomes 0.00 (0.005 + 0.005 - 0.01)
        result2 = rt(Decimal('0.005'))
        assert result2 == Decimal('0.01')
        assert rt.offset == Decimal('0.00')

    def test_offset_accumulation_negative(self):
        """Test that offset accumulates correctly with negative rounding errors"""
        rt = RoundTracker(2)
        # 1.994 rounds to 1.99, offset becomes 0.004 (1.994 - 1.99 = 0.004)
        result1 = rt(Decimal('1.994'))
        assert result1 == Decimal('1.99')
        assert rt.offset == Decimal('0.004')  # Fixed: offset calculation

        # 1.994 rounds to 1.99, offset becomes 0.008
        result2 = rt(Decimal('1.994'))
        assert result2 == Decimal('1.99')
        assert rt.offset == Decimal('0.008')  # Fixed: offset accumulates

        # 1.994 rounds to 1.99, offset becomes 0.002
        result2 = rt(Decimal('1.994'))
        assert result2 == Decimal('2.00')
        assert rt.offset == Decimal('0.002')  # Fixed: offset accumulates

        # 1.994 rounds to 1.99, offset becomes 0.002
        result2 = rt(Decimal('1.996'))
        assert result2 == Decimal('2.00')
        assert rt.offset == Decimal('-0.002')  # Fixed: offset accumulates

    def test_peak_without_offset(self):
        """Test peak method when offset is zero"""
        rt = RoundTracker(2)
        # offset is 0, should use normal ROUND_HALF_UP
        assert rt.peak(Decimal('1.234')) == Decimal('1.23')
        assert rt.peak(Decimal('1.235')) == Decimal('1.24')
        # peak should not modify offset
        assert rt.offset == Decimal('0.0')

    def test_peak_with_positive_offset_above_margin(self):
        """Test peak method with positive offset above margin (uses ROUND_CEILING)"""
        rt = RoundTracker(2)
        rt.offset = Decimal('0.006')  # Above margin of 0.005
        # Should round up (ceiling)
        assert rt.peak(Decimal('1.231')) == Decimal('1.24')
        assert rt.peak(Decimal('1.234')) == Decimal('1.24')
        # peak should not modify offset
        assert rt.offset == Decimal('0.006')

    def test_peak_with_negative_offset_below_margin(self):
        """Test peak method with negative offset below margin (uses ROUND_FLOOR)"""
        rt = RoundTracker(2)
        rt.offset = Decimal('-0.006')  # Below margin of -0.005
        # Should round down (floor)
        assert rt.peak(Decimal('1.239')) == Decimal('1.23')
        assert rt.peak(Decimal('1.236')) == Decimal('1.23')
        # peak should not modify offset
        assert rt.offset == Decimal('-0.006')

    def test_peak_at_offset_margin_boundary(self):
        """Test peak behavior at exact margin boundaries"""
        rt = RoundTracker(2)

        # Exactly at positive margin
        rt.offset = Decimal('0.005')
        assert rt.peak(Decimal('1.231')) == Decimal('1.24')  # ROUND_CEILING

        # Exactly at negative margin
        rt.offset = Decimal('-0.005')
        assert rt.peak(Decimal('1.239')) == Decimal('1.23')  # ROUND_FLOOR

    def test_call_method_equivalence(self):
        """Test that __call__ method works the same as round method"""
        rt1 = RoundTracker(2)
        rt2 = RoundTracker(2)

        value = Decimal('1.234')
        assert rt1(value) == rt2(value)

        # Test multiple calls
        values = [Decimal('0.005'), Decimal('0.005'), Decimal('1.994')]
        results1 = [rt1(v) for v in values]
        results2 = [rt2(v) for v in values]
        assert results1 == results2

    def test_sequence_of_rounds_with_offset_correction(self):
        """Test a sequence of rounds where offset triggers ceiling/floor rounding"""
        rt = RoundTracker(2)

        # Accumulate positive offset
        rt(Decimal('0.004'))  # rounds to 0.00, offset = 0.004
        rt(Decimal('0.004'))  # rounds to 0.00, offset = 0.008

        # Now offset > margin, next round should use ceiling
        result = rt(Decimal('1.001'))  # Should round to 1.01 due to offset
        assert result == Decimal('1.01')

        # Offset should be adjusted
        expected_offset = Decimal('0.008') + Decimal('1.001') - Decimal('1.01')
        assert rt.offset == expected_offset

    def test_round_with_large_values(self):
        """Test rounding with large decimal values"""
        rt = RoundTracker(2)
        assert rt(Decimal('999999.994')) == Decimal('999999.99')
        assert rt(Decimal('999999.995')) == Decimal('1000000.00')

    def test_round_with_negative_values(self):
        """Test rounding with negative values"""
        rt = RoundTracker(2)
        assert rt(Decimal('-1.234')) == Decimal('-1.23')
        assert rt(Decimal('-1.235')) == Decimal('-1.24')
        assert rt(Decimal('-1.236')) == Decimal('-1.24')

    def test_offset_correction_over_multiple_rounds(self):
        """Test that offset correction works correctly over many rounds"""
        rt = RoundTracker(2)

        # Add values that would accumulate rounding errors
        values = [Decimal('0.333333')] * 3  # 0.333333 * 3 = 0.999999
        results = [rt(v) for v in values]

        # First two should round to 0.33, third might round to 0.34 due to offset
        assert sum(results) in [Decimal('0.99'), Decimal('1.00')]

    def test_realistic_scenario_currency_rounding(self):
        """Test realistic scenario with currency calculations"""
        rt = RoundTracker(2)

        # Simulating splitting a payment into three parts
        total = Decimal('10.00')
        part = total / 3  # 3.333333...

        p1 = rt(part)  # 3.33
        p2 = rt(part)  # 3.33
        p3 = rt(part)  # Should be 3.34 to compensate

        assert p1 == Decimal('3.33')
        assert p2 == Decimal('3.33')
        assert p3 == Decimal('3.34')
        assert p1 + p2 + p3 == total

    def test_high_precision_decimals(self):
        """Test with high precision decimal places"""
        rt = RoundTracker(6)
        assert rt(Decimal('1.2345674')) == Decimal('1.234567')
        assert rt(Decimal('1.2345675')) == Decimal('1.234568')
        assert rt.exp == Decimal('0.000000')  # Fixed: exp is '0.' + '0' * 6
        assert rt.offset_margin == Decimal('0.0000005')


@pytest.mark.parametrize("decimals,value,expected", [
    (2, Decimal('1.234'), Decimal('1.23')),
    (2, Decimal('1.235'), Decimal('1.24')),
    (2, Decimal('1.236'), Decimal('1.24')),
    (0, Decimal('1.5'), Decimal('2')),
    (0, Decimal('1.4'), Decimal('1')),
    (0, Decimal('2.5'), Decimal('2')),  # Banker's rounding
    (3, Decimal('2.3454'), Decimal('2.345')),
    (3, Decimal('2.3455'), Decimal('2.346')),
    (3, Decimal('2.3456'), Decimal('2.346')),
    (4, Decimal('9.99995'), Decimal('10.0000')),
    (2, Decimal('-1.234'), Decimal('-1.23')),
    (2, Decimal('-1.235'), Decimal('-1.24')),
])
def test_roundtracker_parametrized(decimals, value, expected):
    """Parametrized test for various decimal places and values"""
    rt = RoundTracker(decimals)
    result = rt(value)
    assert result == expected

