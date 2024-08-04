Feature: Configure digest
    As a user
    I want to personalize my digests configuration
    Such that content quantity and schedule match my needs

    Scenario: Successfully reconfigure a digest
        Given a previous configuration
        When I send new configuration parameters
        Then the configuration is updated
