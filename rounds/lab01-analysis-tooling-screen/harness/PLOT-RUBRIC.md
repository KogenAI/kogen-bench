# Plot semantic rubric (frozen)

Review the rendered `token_cost.png` or `token_cost.svg` after the numeric checker finishes. Use this rubric for every scored output, including smoke qualification. The review is visual and does not award points for a valid file alone.

Record each item as pass/fail and keep a short evidence note:

1. All 16 host-condition observations are visible, or coincident points are explicitly disclosed. If points overlap, the display still communicates the overlap rather than implying fewer observations.
2. The horizontal axis is labelled with the final score and `/106` units.
3. The vertical axis is labelled with total tokens and millions as the unit.
4. Language is visibly encoded and has a matching legend.
5. Condition is visibly encoded and has a matching legend.

`plot_semantic_ok` is true only when all five items pass. A valid PNG header or parseable SVG is only `plot_file_ok`; it does not substitute for this review.
