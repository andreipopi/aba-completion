from ast import arguments
from errno import EHOSTUNREACH
from pydoc import cli
import sys
import random
import numpy as np
from collections import defaultdict, deque

from itertools import chain, combinations, count, islice
import copy
import random
import time
import os
import re


import ast

#used to check that not 2 derivable conclusions in an arg
def get_all_conclusions(assumptions, derived, applied, rules, body_map, head_map):

    cset = []
    for atom in derived:
        if atom not in assumptions:
            in_body_of_triggered = False

            for r in rules:

                if r in applied:
                    if atom in body_map[r]:
                        in_body_of_triggered = True
            
            if in_body_of_triggered == False:
                #print("body of trigerred: ", r[2], "atom: ", atom)
                cset.append(atom)

    return cset


def reconstruct(clingo_output):
    #print(clingo_output)

    #clingo_output = clingo_output+"argument(arg960).\n argument(arg961). \n argument(arg962).\n argument(arg963).\n argument(arg500)."
    #clingo_output = clingo_output+"assumption(29).\n assumption(10). \n assumption(7). \n assumption(19). \n assumption(16).\n assumption(12)."
    matches = re.findall(r'(\w+)\(([^\)]+)\)', clingo_output)
    derivable_atoms_by_arg = defaultdict(set)  # arg_id → set of atoms
    body_map = defaultdict(set)               # rule → set of body atoms
    head_map = {}                             # rule → head atom
    atom_to_rule = {}                         # atom → rule (1-to-1 mapping)
    conclusions = set()                       # set of conclusion atoms
    learnable = set()                         # set of learnable rule names
    all_assumptions = set()

    arg_names = set()
    
    arg_rules_dict = {}
    arg_conclusion = {}

    used_r_ids = []
    # Parse facts
    for pred, args in matches:
        pred = pred.replace(" ", "")
        args = args.replace(" ", "")

        if pred == 'derivable':
            atom, arg_id = args.split(',')
            derivable_atoms_by_arg[arg_id].add(atom)

        elif pred == 'argument':
            arg_names.add(args.strip())

        elif pred == 'assumption':
            all_assumptions.add(args.strip())

        elif pred == 'body':
            rule, atom = args.split(',')
            body_map[rule].add(atom)

        elif pred == 'rule':
            rule, argument = args.split(',')

            used_r_ids.append(rule)
            if argument not in arg_rules_dict.keys():
                arg_rules_dict[argument] = [rule]
            
            if rule not in arg_rules_dict[argument]:
                arg_rules_dict[argument].append(rule)

        elif pred == 'head':
            rule, atom = args.split(',')
            head_map[rule] = atom
            atom_to_rule[atom] = rule  # single rule per atom

        elif pred == 'conclusion':
            conc, arg = args.split(',')
            conclusions.add(conc.strip())

        elif pred == 'learnable':
            learnable.add(args.strip())

    print(atom_to_rule)
    print(head_map)
    print(body_map)
    print(arg_rules_dict)

    
    #some rules have been guessed but are not actuall used
    #so we need to remove them from the mappings.

    headcopy= copy.deepcopy(head_map)
    for rule, head in headcopy.items():

        if rule not in used_r_ids:
            del head_map[rule]
            del body_map[rule]

    # Collect all rules
    rules = []
    learned_rules = []
    # print(all_assumptions)
    # print(conclusions)
    # print(head_map)
    # print(body_map)
    # print(learnable)
    # print(arg_names)
    # print(arg_rules_dict)
    # print(derivable_atoms_by_arg)
    reconstruct_args =[]
    for rule_name, head in head_map.items():
        rule = [rule_name, head] + list(body_map[rule_name])
        if rule_name in learnable:
            learned_rules.append(rule)
        else:
            rules.append(rule)
   
    for arg_name in arg_names:

        completion_derivable = derivable_atoms_by_arg[arg_name]

        arg_conclusion = ""
        for c in conclusions:
            if c in completion_derivable:
                arg_conclusion = c

        assumptions = []

        for atom in completion_derivable:
            if atom in all_assumptions:
                assumptions.append(atom)

      
        derived = [] #for checking if argument in completion is actually an argument
        
        for asm in assumptions:
            derived.append(asm)
        applied = []
        fixed_point = False

        rules_copy = copy.deepcopy(arg_rules_dict[arg_name])
        while fixed_point == False:
            some_rule_applied = False
            #print("derived: ", derived)
            for r in rules_copy :
               
                #print("r: ", r, "head: ", head_map[r], "body: ",  body_map[r])
                body_derived = True

                for b in body_map[r]:
                    if str(b) not in derived:
                        body_derived = False
        
                if body_derived:
                    #print("DERIVED")
                    derived.append(head_map[r])
                    rules_copy.remove(r)
                    applied.append(r)
                    some_rule_applied = True

            if some_rule_applied == False:
                fixed_point = True

        
        #print("applied: ", applied)
        used = []
        for asm in assumptions:
            #print("asm: ", asm)
            for r in arg_rules_dict[arg_name]:
                #print("r: ", r)
                if r in applied:
                    if asm in body_map[r]:
                        if asm not in used:
                            used.append(asm)
        count = 0
        for asm in assumptions:
            if asm not in used:
                count += 1


        used = []
        for asm in completion_derivable:
            if asm != arg_conclusion:
                #print("asm: ", asm)
                for r in arg_rules_dict[arg_name]:
                    #print("r: ", r)
                    if r in applied:
                        if asm in body_map[r]:
                            if asm not in used:
                                used.append(asm)
        for asm in completion_derivable:
            if asm != arg_conclusion:
                if asm not in used:
                    count += 1

        derived_conclusions = get_all_conclusions(assumptions, derived, applied, arg_rules_dict[arg_name], body_map, head_map)


        # print("used: ", used)
        # print(count)

        if count == 0 and len(derived_conclusions) == 1:
            reconstruct_args.append([[derived],[applied],[arg_conclusion]])

    return reconstruct_args,rules+learned_rules


def get_original_rules(original_instance_path, target_rules_ids):
    rules = []
    with open(original_instance_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            line = ''.join(line.split())
            if line.startswith('rule('):
                num = line[len('rule('):-2]
                
                if num in target_rules_ids:
                    rules.append([[num],[],[]])


        for r in rules:
            rule_name = r[0][0]  # e.g., 'r195'
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
    return rules


def difference(completion_rules, selected_instance_path, original_instance_path):
    dif = 0

    print(completion_rules)

    temp = copy.deepcopy(completion_rules)
    completion_keptrules_ids = []

    for rule in temp:
        if "r" in rule[0]:
            completion_keptrules_ids.append(rule[0])
            completion_rules.remove(rule)
    print("aaaaaaaa")
    print(completion_keptrules_ids)  
    print(completion_rules)


    target_rules_ids = []
    with open(selected_instance_path, 'r') as f:
        for line in  f.readlines():
            arg = ast.literal_eval(line)
            for r in arg[1][0]: #for some reason its nested so [0]
                if r not in completion_keptrules_ids:
                    target_rules_ids.append(r)


    print("target_rules: ", target_rules_ids)

    original_target_rules = get_original_rules(original_instance_path, target_rules_ids)
    
    for cr in completion_rules:
        print(cr)
        for orig in original_target_rules:
            if cr[1] == orig[1][0]:
                print("SAME HEAD")
                for b in orig[2][0]:
                    if b not in cr[2]:
                        dif += 1
                for b2 in cr[2]:
                    if b2 not in orig[2][0]:
                        dif += 1

    return dif

def reconstruct_args(input_file_path, dir_rcnstr, dir_rules, dir_selected, dir_original):

    with open(input_file_path, 'r') as infile:


        for line in infile:
            if 'OPTIMUM FOUND' in line:
                parts = line.strip().split(', ')
                instance_name = parts[0]
                instance_name = instance_name.replace(".lp","")

                selected_instance_path = os.path.join(dir_selected, parts[0])


                or_instance_name = parts[0].replace("arg","")
                original_instance_path = os.path.join(dir_original, or_instance_name)

                
                clingo_output = parts[-1]
                arguments, all_used_rules = reconstruct(clingo_output)
                
               
                all_used_rules_copy = copy.deepcopy(all_used_rules)
                diff = difference(all_used_rules_copy, selected_instance_path, original_instance_path)

                for arg in arguments:
                    print(arg)
                output_args_file = os.path.join(dir_rcnstr, instance_name + ".txt")
                output_rules_file = os.path.join(dir_rules, instance_name + ".txt")

                with open(output_args_file, 'w') as outfile:
                    for arg in arguments:
                        outfile.write(f"{arg}\n")
                    outfile.write(str(diff)+"\n")
                    
                
                with open(output_rules_file, 'w') as outfile:
                    for r in all_used_rules:
                        outfile.write(f"{r}\n")
                       

# Example usage:
#INPUT looks like 
# argaba_100_0.1_10_10_2.lp, clingo, UNSATISFIABLE, #   total CPU user time (s): 0.450774, NO ANSWER
# argaba_100_0.1_10_10_3.lp, clingo, OPTIMUM FOUND, #   total CPU user time (s): 0.138006, assumption(7) conclusion(41) conclusion(44) usable_atom(92) body(r75,7) body(r159,25) body(r182,92) derivable(7,arg41) derivable(25,arg41) derivable(41,arg41) head(r75,25) head(r159,41) head(r182,44) in_argument(41,arg41) in_argument(25,arg41) in_argument(7,arg41) in_argument(44,arg44) in_argument(92,arg44) reach(25,41,arg41) reach(7,41,arg41) reach(7,25,arg41) reach(92,44,arg44) learnable(2) learnable(12) lhead(2,25) lhead(12,92) lbody(12,25) lbody(2,7) lbody(12,7) in_argument(25,arg44) in_argument(7,arg44) reach(25,44,arg44) reach(25,92,arg44) reach(7,25,arg44) reach(7,44,arg44) reach(7,92,arg44) derivable(7,arg44) derivable(44,arg44) derivable(92,arg44) derivable(25,arg44)
# argaba_100_0.1_10_10_4.lp, clingo, UNSATISFIABLE, #   total CPU user time (s): 0.038047, NO ANSWER
# argaba_100_0.1_10_10_5.lp, clingo, OPTIMUM FOUND, #   total CPU user time (s): 0.562048, assumption(10) assumption(2) conclusion(36) conclusion(79) conclusion(17) usable_atom(61) usable_atom(79) body(r486,10) body(r241,92) body(r263,55) body(r9,2) body(r35,12) derivable(10,arg36) derivable(2,arg17) derivable(92,arg36) derivable(12,arg17) derivable(55,arg36) derivable(17,arg17) head(r486,92) head(r241,55) head(r263,58) head(r9,12) head(r35,17) in_argument(36,arg36) in_argument(92,arg36) in_argument(10,arg36) in_argument(55,arg36) in_argument(58,arg36) in_argument(79,arg79) in_argument(17,arg17) in_argument(12,arg17) in_argument(2,arg17) reach(92,55,arg36) reach(92,58,arg36) reach(55,58,arg36) reach(10,92,arg36) reach(10,55,arg36) reach(12,17,arg17) reach(2,17,arg17) reach(2,12,arg17) reach(10,58,arg36) derivable(58,arg36) learnable(14) learnable(15) lhead(14,36) lhead(15,79) lbody(14,58) lbody(15,2) in_argument(2,arg79) reach(92,36,arg36) reach(55,36,arg36) reach(58,36,arg36) reach(10,36,arg36) reach(2,79,arg79) derivable(2,arg79) derivable(36,arg36) derivable(79,arg79)
# argaba_100_0.1_10_10_6.lp, clingo, UNSATISFIABLE, #   total CPU user time (s): 0.071095, NO ANSWER

reconstruct_args('/Users/andreipopi/Documents/GitLab/discover-aba/Experiments/compiled_results_100_prefrand-run2/clingo/clingo_results.txt', 
                        '/Users/andreipopi/Documents/GitLab/discover-aba/Experiments/completed_args_100_prefrand-run2', 
                        '/Users/andreipopi/Documents/GitLab/discover-aba/Experiments/completed_rules_100_prefrand-run2', 
                        '/Users/andreipopi/Documents/GitLab/discover-aba/InstanceGenerator/datasets_final/selected_in_100_12345',
                        "/Users/andreipopi/Documents/GitLab/discover-aba/InstanceGenerator/iccma/iccma_as_asp_100")





