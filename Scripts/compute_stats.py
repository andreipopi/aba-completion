import statistics
import os

def summarize_results_with_argument_size(results_file, size_dir, completed_dir):
    timeouts = 0
    unsat = 0
    solved = 0
    total_instances = 0
    times = []
    conclusion_counts = []
    table_data = []

    with open(results_file, 'r') as file:
        for line in file:
            total_instances += 1
            line_upper = line.strip().upper()

            if "TIMEOUT" in line_upper:
                timeouts += 1
            elif "UNSATISFIABLE" in line_upper:
                unsat += 1
            elif "OPTIMUM FOUND" in line_upper:
                solved += 1

                count_conclusions = line_upper.count("CONCLUSION(")
                conclusion_counts.append(count_conclusions)

                try:
                    time_str = line_upper.split("TOTAL CPU USER TIME (S):")[1].split(",")[0].strip()
                    time_val = float(time_str)
                    times.append(time_val)
                except:
                    time_val = None

                instance_name = line.split(",")[0].strip()
                size_file_path = os.path.join(size_dir, f"size_{instance_name}")

                import copy
                iname = copy.deepcopy(instance_name)
                iname = copy.deepcopy(iname.replace(".lp",".txt"))
                distance_file_path = os.path.join(completed_dir, iname)
                dist = 0
                with open(distance_file_path, 'r') as df:
                    last_line = [line.strip() for line in df if line.strip()][-1]
                    dist = last_line

                try:
                    with open(size_file_path, 'r') as sf:
                        lines = sf.readlines()
                        size = int(lines[0].strip())
                        rule_count = int(lines[5].strip())
                        atom_count = int(lines[4].strip())
                except:
                    size = None
                    rule_count = None
                    atom_count = None

                if time_val is not None and size is not None and rule_count is not None and atom_count is not None:
                    table_data.append((instance_name, time_val, size, rule_count,atom_count, count_conclusions, dist))

    table_data.sort(key=lambda x: x[1])

    print(f"Total instances: {total_instances}")
    print(f"Solved (OPTIMUM FOUND): {solved}")
    print(f"Timeouts: {timeouts}")
    print(f"UNSATISFIABLE: {unsat}")

    if times:
        print(f"Median solve time: {statistics.median(times):.3f} seconds")
    else:
        print("No solve times found.")

    if conclusion_counts:
        avg_conclusions = sum(conclusion_counts) / len(conclusion_counts)
        print(f"Average number of conclusions: {avg_conclusions:.2f}")
    else:
        print("No conclusions found.")

    print("\nInstance Table (sorted by solve time):")
    print(f"{'instance':<40} {'solve time(s)':<15} {'#atoms (largest arg)':<18} {'#rules':<10} {'#atoms':<10} {'#args':<10} {'distance'}")
    for instance, time_val, size, rule_count, atom_count, conc_count, dist in table_data:
        print(f"{instance:<40} {time_val:<15.3f} {size:<18} {rule_count:<10} {atom_count:<10} {conc_count:<10} {dist}")

summarize_results_with_argument_size(
    "/Users/andreipopi/Documents/GitLab/discover-aba/Experiments/compiled_results_100_prefrand-run2/clingo/clingo_results.txt",
    "/Users/andreipopi/Documents/GitLab/discover-aba/InstanceGenerator/datasets_final/biggest_100_12345",
    "/Users/andreipopi/Documents/GitLab/discover-aba/Experiments/completed_args_100_prefrand-run2"
)