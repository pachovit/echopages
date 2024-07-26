Feature: Add content
    As a user
    I want to add new content
    Such that I can be reminded of it in the future

    Scenario Outline: Successfully add content
        Given a content with source <source>, author <author>, location <location>, and text <text>
        When I add the content
        Then content should be retrievable

            Examples:
            | source    | author     | location  | text    |
            | Book Name | One Author | Chapter 1 | summary |
