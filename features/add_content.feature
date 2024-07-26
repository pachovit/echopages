Feature: Add content
    As a user
    I want to add new content
    Such that I can be reminded of it in the future

    Scenario Outline: Successfully add content
        Given a content with source <source>, author <author>, location <location>, and text <text>
        When I add the content
        Then content should be retrievable

        Examples:
            | source    | author     | location  | text                                      |
            | Book Name | One Author | Chapter 1 | summary                                   |
            | <none>    | <none>     | <none>    | Book Name One Author Chapter 1 summary    |
    
    Scenario Outline: Not adding content when not specifying text
        Given a content without text, with source <source>, author <author>, location <location>
        When I add the content without text
        Then a 400 error should be raised

        Examples:
            | source    | author     | location  |
            | Book Name | One Author | Chapter 1 |