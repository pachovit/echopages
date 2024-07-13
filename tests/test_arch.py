from pytestarch import Rule, get_evaluable_architecture

SRC_DIR = "echopages.echopages"

evaluable = get_evaluable_architecture("../echopages", "../echopages/echopages")


def module_should_not_depend(module_1, module_2):
    """
    Module 1 should not depend on module 2
    """
    rule = (
        Rule()
        .modules_that()
        .are_sub_modules_of(f"{SRC_DIR}.{module_2}")
        .should_not()
        .be_imported_by_modules_that()
        .are_sub_modules_of(f"{SRC_DIR}.{module_1}")
    )

    rule.assert_applies(evaluable)


def test_architecture():
    module_should_not_depend("domain", "application")
    module_should_not_depend("domain", "infrastructure")
    module_should_not_depend("application", "infrastructure")
