from ast import arguments
from errno import EHOSTUNREACH
import sys
import random
import numpy as np
from itertools import chain, combinations, count, islice
import copy
import random
import time

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in [5])

# def powerset(iterable, max_subsets=5000):
#     s = list(iterable)
#     all_combos = chain.from_iterable(combinations(s, r)for r in [1,2,3,4,5,6,7])
#     return islice(all_combos, max_subsets)


# def powerset(iterable, max_subsets=1000, max_size=8):
#     s = list(iterable)
#     # Generate all combinations of size 0 to max_size
#     combo_generator = chain.from_iterable(combinations(s, r) for r in range(max_size + 1))
#     # Take only the first max_subsets combinations
#     return list(islice(combo_generator, max_subsets))

# def powerset(iterable, subset_size=7):
#     s = list(iterable)
#     return chain.from_iterable(combinations(s, subset_size))

def conclusions(assumptions, derived, applied, rules):

   
    cset = []
    for atom in derived:
        
        if atom not in assumptions:
            in_body_of_triggered = False

            for r in rules:

                if r[0][0] in applied:
                    if atom in r[2]:
                        in_body_of_triggered = True
            
            if in_body_of_triggered == False:
                #print("body of trigerred: ", r[2], "atom: ", atom)
                cset.append(atom)

    return cset

    
# dont consider assumptions as arguments
# arguments are full derivation up to top
def construct_arguments(assumptions,rules):
    #assumptions = ["a","b","c"]
    #print("powerset: ", list(powerset(assumptions)))
    #[asumpptions][atoms][rules]
    #[[derived],[rules],[conclusion]]
    arguments = []
    print("in")
    #sets = list(powerset(assumptions))

    sets = powerset(assumptions)

    print("out")
   

  
    
    start_time = time.time()  # start timer

    for set in sets:

        derived = []
        applied = []

        #rules = [[["r0"],["y"],["a","b"]],[["r1"],["x"],["b","c"]],[["r2"],["z"],["y"]],[["r3"],["w"],["x"]],[["r4"],["k"],["c"]]]
        rules_copy = copy.deepcopy(rules)

        for asm in set:
            derived.append(asm)

        fixed_point = False

        print(derived)
        while fixed_point == False:
            some_rule_applied = False

            for r in rules_copy:

                if r[1][0] not in derived: #if a rule for this head wasnt already applied

                    print("assumption set: ", set)
                    print("r: ", r)
                    body_derived = True

                    for b in r[2]:
                        if b not in derived:
                            body_derived = False
            
                    if body_derived:
                        print("DERIVED")
                        derived.append(r[1][0])
                        rules_copy.remove(r)
                        applied.append(r[0][0])
                        some_rule_applied = True

            if some_rule_applied == False:
                fixed_point = True

        conc = conclusions(set, derived, applied, rules)

        if len(conc) == 1:
            print("----Argument---",set, "--",derived,"--", conc)
            #print("applied: ", applied)

           
            used = []
            for asm in set:
                for r in rules:
                    if r[0][0] in applied:
                        if asm in r[2]:
                            if asm not in used:
                                used.append(asm)
            count = 0
            for asm in set:
                if asm not in used:
                    count += 1
            # print("used: ", used)
            # print(count)


            if count == 0:
                arguments.append([[derived],[applied],[conc]])
            
            # if len(arguments) == 10:
            #     return arguments
        if time.time() - start_time > 300:
            return arguments

   
    return arguments
    #return [arg for arg in arguments if (len(arg[2][0]) == 1)]


# with open(sys.argv[1], 'r') as file:
#     lines = file.readlines()

import os 

input_folder = "/home/andreipopi/Documents/GitLab/discover-aba/InstanceGenerator/iccma/iccma_as_asp_500"

#output_dir = "constructed_arguments"
output_dir = "/home/andreipopi/Documents/GitLab/discover-aba/InstanceGenerator/constructed_arguments_500_5"

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_folder):
    if not filename.endswith(".lp"):
        continue

    finalname=f"arg{filename}" 
    
    if not finalname in os.listdir(output_dir):
        

        print(filename)
        input_path = os.path.join(input_folder, filename)
        with open(input_path, 'r') as file:
            lines = file.readlines()

        assumptions = []
        atoms = []
        rules = []

    

        for line in lines:
            line = line.strip()
            line = ''.join(line.split())

            if line.startswith('assumption('):
                num = str(line[len('assumption('):-2])
                assumptions.append(num)
            elif line.startswith('atom('):
                num = str(line[len('atom('):-2])
                atoms.append(num)
            
            elif line.startswith('rule('):
                num = line[len('rule('):-2]
                rules.append([[num],[],[]])


        for r in rules:
            rule_name = r[0][0]  # e.g., 'r195'
            #print("rule name: ", rule_name)
            head_prefix = f"head({rule_name},"
            body_prefix = f"body({rule_name},"
            
            for line in lines:
                line = line.strip()
                line = ''.join(line.split())

                if line.startswith(head_prefix):
                    num = line[len(head_prefix):-2]  # removes trailing ').\n' or ').'
                    r[1].append(num)
                elif line.startswith(body_prefix):
                    num = line[len(body_prefix):-2]
                    r[2].append(num)
        
   
        # print("Assumptions:", assumptions)
        # print("Atoms:", atoms)
        # print("Rules: ",rules)


        args = construct_arguments(assumptions,rules)

        os.makedirs(output_dir, exist_ok=True)

        #input_filename = os.path.basename(sys.argv[1])

        output_filename = os.path.join("constructed_arguments_500_5", f"arg{filename}")

        with open(output_filename, 'w') as f:
            f.write("Derived , rules applied, conclusion\n")
            for argument in args:
                f.write(str(argument) + "\n")

        print("Derived , rules applied, conclusion")
        for argument in args:
            print(argument)









