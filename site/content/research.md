## What we are testing

Kogen is being built at [Optimum Tech](https://optimum.ba) to carry a shaped software feature through implementation, checks, review and rework. Bench records the experiments that inform that work.

- **Models and reasoning effort.** Which combinations finish the task correctly, how long they take, and what they cost.
- **Plans and context.** How much detail a builder needs, and whether a prepared packet of relevant project information helps it work.
- **Agent design.** The prompts, tools and execution loops around a model, including comparisons involving Kogen, Codex and Grok Build. Each record states what actually ran.
- **Checks and recovery.** How we grade working software, where review helps or gets in the way, and what to do when a build fails.
- **Languages and implementation choices.** Experiments across Rust, Go, TypeScript and Elixir, with task and environment differences kept visible.

## Hill-climbing, with a record of the steps

Hill-climbing means making a change, measuring what happens, and using that result to choose the next experiment. We have been testing plan detail, prepared context, builder strength and other choices in the software-building process.

A promising result is a reason to test again. Our [context-packet pilot](/rounds/l4-context-packet/) supported keeping prepared context on its selected tasks; the [independent replication](/rounds/l4b-confirm/) did not confirm an advantage on its new US tasks. Both belong in the record.

The archive also includes [failed-build recovery experiments](/rounds/l3b-repair-vs-continue/) and [cache-key checks](/rounds/cache-key-api-v4/). Further work will test promising changes on fresh tasks and improve the rerun kit. New results will be added after their evidence is reviewed; this is a research direction, not a release schedule.
