// Standing research disclaimer shown on every participant-facing page, per
// experiment_spec.md §8 ("Research disclaimers... Page 1 must state...").
export default function ResearchDisclaimer() {
  return (
    <div className="disclaimer">
      <strong>Research prototype, not real care.</strong> This is a concept test for
      research purposes only. No medical care is being delivered, no diagnosis or
      treatment is provided, and no personal health information is required. Your
      responses are used only for this research study.
    </div>
  );
}
