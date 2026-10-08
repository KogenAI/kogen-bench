# About Kogen Bench

Kogen Bench is the research record behind [Kogen](https://kogen.dev), a coding-agent harness built by [Almir Sarajčić](https://almirsarajcic.com/). It records experiments comparing coding agents, the systems that guide them, and the cost and correctness of their work.

## Who is behind it

Kogen is developed by Almir at [Optimum Tech, LLC](https://optimum.ba). It is under active development. The goal is to let you shape a software feature and approve its plan, then have Kogen carry it through implementation, checks, independent review, and a resulting commit.

This research site is maintained as part of that work. For inquiries, email [contact@kogen.dev](mailto:contact@kogen.dev).

## The work behind the record

We test model and effort choices, plans, project context, agent execution loops, checks, recovery and implementation languages. Hill-climbing connects those experiments: change part of the process, measure the result, then decide what to test next. Fresh tasks and replication help check whether a promising change holds up.

The [homepage](/) introduces these research questions. The round pages distinguish completed experiments from designs, withdrawn work and results still being checked.

## Reading the evidence

Start with the [findings](/findings/), then follow the [hypotheses](/hypotheses/) to the [experiment records](/rounds/). Each round is the authority for its own design, history, outcomes, and limits. Designs are identified as pre-registered or retrospective; descriptive results keep their label.

The site is generated from the public repository. Pages link to the source revision behind the snapshot, and [data downloads](/data/) preserve the distinction between official outcomes and captured deliveries. Missing values and incomplete records remain visible.

## Source and reproduction

The [repository](https://github.com/KogenAI/kogen-bench) is licensed under Apache-2.0 with closed contributions: it does not accept issues or pull requests. Kogen brand assets are not covered by that software license.

The [reproduction guide](/reproduce/) explains which public exports can be rebuilt and which executions cannot be replayed. Available task bases, hidden suites and graders are published for inspection and post-run grading. Hidden means kept from the agent during execution. The [verification guide](/verify/) and [rerun guide](/rerun/) state what is available and what remains incomplete. See [credits](/credits/) for the upstream projects behind the tasks. [Kogen.dev](https://kogen.dev) owns product information; this site owns the research presentation.
