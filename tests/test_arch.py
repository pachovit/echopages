import pytestarch

SRC_DIR = "echopages.echopages"

evaluable = pytestarch.get_evaluable_architecture(
    "../echopages", "../echopages/echopages"
)


def module_should_not_depend(module_1: str, module_2: str) -> None:
    """Module 1 should not depend on module 2."""
    rule = (
        pytestarch.Rule()
        .modules_that()
        .are_sub_modules_of(f"{SRC_DIR}.{module_2}")
        .should_not()
        .be_imported_by_modules_that()
        .are_sub_modules_of(f"{SRC_DIR}.{module_1}")
    )

    rule.assert_applies(evaluable)


def test_architecture() -> None:
    module_should_not_depend("domain", "application")
    module_should_not_depend("domain", "infrastructure")
    module_should_not_depend("application", "infrastructure")
    module_should_not_depend("domain", "api")
    module_should_not_depend("application", "api")
    module_should_not_depend("infrastructure", "api")
