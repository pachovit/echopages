Feature: Add content
    As a user
    I want to add new content
    Such that I can be reminded of it in the future

    Scenario: Successfully add content
        Given the user is on the add content page
        When the user enters valid content text
        And clicks the submit button
        Then the content should be saved
        And content should be retrievable
