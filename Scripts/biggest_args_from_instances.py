import os
import re
from collections import defaultdict

def process_lp_facts(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for fname in os.listdir(input_dir):
        if not fname.endswith(".lp"):
            continue

        in_path = os.path.join(input_dir, fname)
        out_path = os.path.join(output_dir, f"size_{fname}")

        with open(in_path) as f:
            lines = f.readlines()

        derivable_map = defaultdict(list)
        rule_map = defaultdict(list)

        # Track all declared arguments
        arguments = set()
        atom_set = set()
        rule_set = set()

        for line in lines:
            line = line.strip()
            # Find all argument declarations
            match_arg = re.match(r"argument\((arg\d+)\)", line)
            if match_arg:
                arguments.add(match_arg.group(1))

            # Parse inarg predicates
            match_inarg = re.match(r"inarg\(([^,]+),\s*(arg\d+)\)", line)
            if match_inarg:
                atom, arg = match_inarg.groups()
                derivable_map[arg].append((atom, arg))
                atom_set.add(atom)

            # Parse rule predicates
            match_rule = re.match(r"rule\(([^,]+),\s*(arg\d+)\)", line)
            if match_rule:
                rule, arg = match_rule.groups()
                rule_map[arg].append((rule, arg))
                rule_set.add(rule)

        # Identify biggest by derivables
        max_deriv_arg = max(derivable_map.items(), key=lambda x: len(x[1]), default=(None, []))
        max_rule_arg = max(rule_map.items(), key=lambda x: len(x[1]), default=(None, []))

        with open(out_path, "w") as out_file:
            out_file.write(f"{len(max_deriv_arg[1])}\n")
            out_file.write(f"{len(max_rule_arg[1])}\n")
            out_file.write(f"{max_deriv_arg[1]}\n")
            out_file.write(f"{max_rule_arg[1]}\n")
            out_file.write(f"{len(atom_set)}\n")
            out_file.write(f"{len(rule_set)}\n")

# Example usage
input_dir = "/Users/andrei/Documents/GitLab/discover-aba/InstanceGenerator/datasets_final/instances_2000_12345_premeaning"
output_dir = "/Users/andrei/Documents/GitLab/discover-aba/InstanceGenerator/datasets_final/biggest_2000_12345"
process_lp_facts(input_dir, output_dir)