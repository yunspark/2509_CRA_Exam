# https://github.com/jeonghwan-seo/Python-CRA-Example/blob/main/refactoring/function_paramterized.py

class TaxCalculator:
    LOWER_THRESH = 30000.0
    MIDDLE_THRESH = 100000.0
    LOWER_RATIO = 0.1
    MIDDLE_RATIO = 0.2
    UPPER_RATIO = 0.3

    def calculate_tax(self, income: float) -> float:
        tax = 0.0
        for ratio in [TaxCalculator.LOWER_RATIO, TaxCalculator.MIDDLE_RATIO, TaxCalculator.UPPER_RATIO]:
            tax += self._bracket(income, ratio)
        return tax

    def _bracket(self, income: float, ratio: float) -> float:
        if income < TaxCalculator.LOWER_THRESH:
            return self._lower_bracket(income) * ratio
        elif income < TaxCalculator.MIDDLE_THRESH:
            return self._middle_bracket(income) * ratio
        else:
            return self._upper_bracket(income) * ratio

    def _lower_bracket(self, income: float) -> float:
        return min(income, TaxCalculator.LOWER_THRESH)

    def _middle_bracket(self, income: float) -> float:
        return min(income, TaxCalculator.MIDDLE_THRESH) - TaxCalculator.LOWER_THRESH if income > TaxCalculator.LOWER_THRESH else 0

    def _upper_bracket(self, income: float) -> float:
        return income - TaxCalculator.MIDDLE_THRESH if income > TaxCalculator.MIDDLE_THRESH else 0



def test_calculate_tax():
    calc = TaxCalculator()
    assert calc.calculate_tax(15000) == 1500.0
    assert calc.calculate_tax(31000) == 3200
    assert calc.calculate_tax(100200) == 17060