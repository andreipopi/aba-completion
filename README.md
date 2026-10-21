# Completing Structured Arguments in Assumption-Based Argumentation

> [!NOTE]
> This is the maintained GitHub repository for ABA Completion. The project was originally hosted in the [TU Graz Knowledge Representation and Reasoning (KRR) GitLab repository](https://gitlab.tugraz.at/krr/aba-completion).

This repository contains the Answer Set Programming (ASP) encoding and experimental artifacts for the paper **Completing Structured Arguments in Assumption-Based Argumentation**. The encoding completes partial ABA arguments by learning missing rules and atoms while ensuring that the result has a valid tree-based argument structure. Relatedness information can be used to prefer more coherent completions.

## Publication

Andrei Popescu and Johannes P. Wallner. **Completing Structured Arguments in Assumption-Based Argumentation.** In *Logics in Artificial Intelligence - 19th European Conference, JELIA 2025*, Lecture Notes in Computer Science, volume 16093, pages 95-111. Springer, 2026.

- [Published paper](https://doi.org/10.1007/978-3-032-04587-4_7)
- [Author manuscript with supplementary material](paper_with_appendix.pdf)

## Contents

- [`aba-complete-final.lp`](aba-complete-final.lp): ASP encoding for completing partial ABA arguments
- [`instances/`](instances/): generated benchmark instances and supporting metadata
- [`results/`](results/): raw Clingo logs and compiled experimental results
- [`Scripts/`](Scripts/): Python scripts for generating instances and processing results
- [`paper_with_appendix.pdf`](paper_with_appendix.pdf): author manuscript with supplementary material

## Requirements

- [Clingo](https://potassco.org/clingo/)
- Python 3
- [NumPy](https://numpy.org/) for the Python scripts

The experiments were run with Clingo 5.6.2. The command below was also tested with Clingo 5.8.0.

## Running the Prototype

From the repository root, solve one of the included instances with:

```bash
clingo aba-complete-final.lp \
  instances/instances_100_12345_prefrand/argaba_100_0.1_10_10_2.lp \
  --opt-mode=opt
```

Use `--opt-mode=optN` to enumerate all optimal completions.

By default, the encoding permits up to 20 learned rules, rule bodies of at most five elements, and six additional candidate atoms. These values can be changed in [`aba-complete-final.lp`](aba-complete-final.lp).

## Experiments

The repository contains 217 benchmark cases derived from ICCMA 2023 ABA frameworks with 100, 500, or 2,000 atoms. Each case is provided in two variants:

- `prefrand`: atoms are assigned to relatedness groups randomly
- `premeaning`: relatedness is based on the rules of the selected arguments

The scripts contain the paths used for the original experiments. Update their input and output paths before running them on another machine.

## Citation

```bibtex
@inproceedings{PopescuWallner2026,
  author    = {Andrei Popescu and Johannes P. Wallner},
  title     = {Completing Structured Arguments in Assumption-Based Argumentation},
  booktitle = {Logics in Artificial Intelligence -- 19th European Conference, JELIA 2025},
  series    = {Lecture Notes in Computer Science},
  volume    = {16093},
  pages     = {95--111},
  publisher = {Springer},
  year      = {2026},
  doi       = {10.1007/978-3-032-04587-4_7}
}
```

## Authors

- Andrei Popescu
- Johannes P. Wallner
