# Top Level Sequence Diagram
Cover Agent consists of many classes but the fundamental flow lives within the CoverAgent and UnitTestGenerator classes. The following is a sequence diagram (written in [Mermaid](https://mermaid.js.org/syntax/sequenceDiagram.html)) depicting the flow of how Cover Agent works and interacts with a Large Language Model.

```mermaid
sequenceDiagram
    participant User
    participant CoverAgent
    participant UnitTestGenerator
    participant CoverageProcessor
    participant AICaller
    participant PromptBuilder

    User->>CoverAgent: Initialize with args
    CoverAgent->>UnitTestGenerator: Initialize UnitTestGenerator
    UnitTestGenerator->>AICaller: Initialize AICaller
    UnitTestGenerator->>CoverageProcessor: run_coverage()
    CoverageProcessor-->>UnitTestGenerator: Return coverage metrics

    CoverAgent->>UnitTestGenerator: initial_test_suite_analysis()

    loop Test generation and validation
        CoverAgent->>UnitTestGenerator: generate_tests()
        UnitTestGenerator->>PromptBuilder: build_prompt(test_generation_prompt)
        PromptBuilder-->>UnitTestGenerator: Return prompt
        note right of UnitTestGenerator: Request in prompt: <br/>1. Analyze source file <br/>2. Analyze test file <br/>3. Generate new unit tests to increase coverage <br/>4. Follow provided guidelines for test generation: <br />a. Carefully analyze the provided code <br />b. Understand its purpose, inputs, outputs, and key logic <br />c. Brainstorm necessary test cases <br />d. Review tests for full coverage <br />e. Ensure consistency with existing test suite
        PromptBuilder-->>AICaller: Construct and return full prompt
        UnitTestGenerator->>AICaller: Call model to generate tests
        note right of AICaller: Instructions: <br/>1. Analyze provided files <br/>2. Generate new tests <br/>3. Provide YAML object with new tests including: <br />a. Test behavior <br />b. Lines to cover <br />c. Test name <br />d. Test code <br />e. New imports <br />f. Test tags
        AICaller-->>UnitTestGenerator: Return generated tests

        UnitTestGenerator->>UnitTestGenerator: validate_test()
        note right of UnitTestGenerator: Append and run generated tests
        note right of UnitTestGenerator: Check test results

        alt Test failed
            UnitTestGenerator->>UnitTestGenerator: Rollback test file
            UnitTestGenerator->>UnitTestGenerator: Append failure details
        else Coverage not increased
            UnitTestGenerator->>UnitTestGenerator: Rollback test file
            UnitTestGenerator->>UnitTestGenerator: Append failure details
        else Test passed and coverage increased
            UnitTestGenerator->>CoverageProcessor: run_coverage()
            CoverageProcessor-->>UnitTestGenerator: Return updated coverage metrics
        end
    end

    note right of CoverAgent: Generate report
```