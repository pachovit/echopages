Feature: Trigger digest
    As a user
    I want to receive on-demand a digest with content
    Such that I can review some of my content

    Scenario: Successfully trigger a digest
        Given some already added contents
        When I trigger a digest
        Then the digest should be delivered with some content
