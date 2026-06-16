# Further reading

A small, opinionated reading list to go deeper than this handbook does.

## Neuroimaging

- **Poldrack, Mumford, Nichols — *Handbook of fMRI Data Analysis*** (Cambridge). Still the best on-ramp to fMRI thinking even if some tooling has moved on.
- **Jones — *Diffusion MRI: Theory, Methods, and Applications*** (Oxford). The reference for understanding what DWI signals actually represent.
- **The BIDS specification** — <https://bids-specification.readthedocs.io>. Read the introduction; skim the rest; come back when you have a specific question.
- **The Neurostars forum** — <https://neurostars.org>. Where most BIDS and BIDS-apps questions get answered.

## Data engineering

- **Kleppmann — *Designing Data-Intensive Applications*** (O'Reilly). The single most useful book for someone moving into data infrastructure. Read it twice.
- **Reis & Housley — *Fundamentals of Data Engineering*** (O'Reilly). Maps the modern landscape end-to-end.
- **The dbt documentation** — <https://docs.getdbt.com>. Even if you don't use dbt, the docs teach modern analytics-engineering thinking.
- **The Snakemake tutorial** — <https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html>. The fastest path to DAG-native thinking for someone with a bash background.

## AI / ML for neuroimaging

- **The MONAI documentation** — <https://docs.monai.io>. PyTorch-flavoured medical-imaging library; useful even if you end up writing your own training loops.
- **Litjens et al. — *A Survey on Deep Learning in Medical Image Analysis*** (Medical Image Analysis, 2017). Older but still orienting.
- **The fastMRI papers** (Facebook AI). Concrete worked examples of reconstruction-focused DL on raw MRI.

## Operating production systems

- **The Google SRE Book** — <https://sre.google/books/>. Free online. The terminology in this book (SLI/SLO/error budgets) is now industry-standard.
- **Beyer et al. — *The Site Reliability Workbook*** (O'Reilly). Companion to the SRE Book, more practical.

---

*Suggestions welcome via PR.*
