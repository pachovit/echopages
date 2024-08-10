Feature: Get all content
    As a user
    I want to retreive all my content
    Such that I can visualize it and manage it

    Scenario: Successfully get all content
        Given 10 content units previously added
        When I request all content
        Then I should get all 10 elements with IDs
