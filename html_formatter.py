import argparse
import os
from os import path
import math

from jinja2 import Environment, FileSystemLoader

SYS1_MATCH = "only_sys1"
SYS2_MATCH = "only_sys2"
BOTH_MATCH = "both"
NEITHER_MATCH = "neither"
ALL = "all"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", default="vis_analysis")
    parser.add_argument("--sys1")
    parser.add_argument("--sys2")
    parser.add_argument(
        "--filter",
        choices={SYS1_MATCH, SYS2_MATCH, BOTH_MATCH, NEITHER_MATCH, ALL},
        default=SYS1_MATCH,
    )

    args = parser.parse_args()

    return args


def get_results(args):
    def condition(sys1_l, sys2_l):
        if args.filter == SYS1_MATCH:
            return sys1_l == "MATCH" and sys2_l != "MATCH"
        elif args.filter == SYS2_MATCH:
            return sys1_l != "MATCH" and sys2_l == "MATCH"
        elif args.filter == BOTH_MATCH:
            return sys1_l == "MATCH" and sys2_l == "MATCH"
        elif args.filter == NEITHER_MATCH:
            return sys1_l != "MATCH" and sys2_l != "MATCH"
        else:
            return True

    os.chdir(args.workspace)

    with open("input.name", "r") as f:
        name_list = f.read().splitlines()
    with open("ref.smiles", "r") as f:
        ref_smiles_list = f.read().splitlines()
    with open(f"{args.sys1}.smiles", "r") as f:
        sys1_smiles_list = f.read().splitlines()
    with open(f"{args.sys1}.scores", "r") as f:
        sys1_score_list = f.read().splitlines()
    with open(f"{args.sys2}.smiles", "r") as f:
        sys2_smiles_list = f.read().splitlines()
    with open(f"labels/{args.sys1}.label", "r") as f:
        sys1_label_list = f.read().splitlines()
    with open(f"labels/{args.sys2}.label", "r") as f:
        sys2_label_list = f.read().splitlines()

    results = []
    for idx, (sys1_l, sys2_l) in enumerate(zip(sys1_label_list, sys2_label_list)):
        if condition(sys1_l, sys2_l):
            name = name_list[idx]
            ref_smiles = ref_smiles_list[idx]
            sys1_smiles = sys1_smiles_list[idx]
            sys1_score = sys1_score_list[idx]
            sys2_smiles = sys2_smiles_list[idx]

            ref_img = f"images/ref/{idx}.svg"
            sys1_img = f"images/{args.sys1}/{idx}.svg"
            sys2_img = f"images/{args.sys2}/{idx}.svg"
            results.append(
                {
                    "name": name,
                    "ref_s": ref_smiles,
                    "ref_img": ref_img,
                    "sys1": args.sys1,
                    "sys1_s": sys1_smiles,
                    "sys1_score": sys1_score,
                    "sys1_img": sys1_img,
                    "sys2": args.sys2,
                    "sys2_s": sys2_smiles,
                    "sys2_img": sys2_img,
                }
            )

    return results


def main():
    args = parse_args()

    env = Environment(loader=FileSystemLoader(path.dirname(__file__)))
    template = env.get_template("template.html")

    data = {"results": get_results(args)}

    print(template.render(data))


if __name__ == "__main__":
    main()
