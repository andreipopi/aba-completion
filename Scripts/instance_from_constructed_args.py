import sys
import os
import random
import numpy as np
import ast



input_folder = "/Users/andrei/Documents/GitLab/discover-aba/InstanceGenerator/argument_construction/constructed_arguments_2000_12345_minustrivial"
# input_folder = "/Users/andrei/Documents/GitLab/discover-aba/InstanceGenerator/constructed_running_example"

output_dir =             "instances_2000_12345_premeaning" # instances themselves
output_dir_random =      "instances_2000_12345_prefrand" # instances themselves
output_dir_constructed = "selected_in_2000_12345" #store the 10 selected constructed arguments for each instance

# output_dir =             "running_instance_premeaning" # instances themselves
# output_dir_random =      "running_instance_prefrand" # instances themselves
# output_dir_constructed = "selected_in_running" #store the 10 selected constructed arguments for each instance

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_folder):
    filename_wo_ext = os.path.splitext(filename)[0]  # 'argaba_100_0.1_5_5_3'
    filename_wo_ext = filename_wo_ext[3:]
    original_instance = "/Users/andrei/Documents/GitLab/discover-aba/InstanceGenerator/iccma/iccma_as_asp_2000"+"/"+filename_wo_ext+".lp"

    #original_instance = "/Users/andrei/Documents/GitLab/discover-aba/InstanceGenerator/running/running_example_copy.lp"

    # full_path = sys.argv[1]
    # filename = os.path.basename(full_path)  # e.g., 'argaba_100_0.1_5_5_3.lp'
    # filename_wo_ext = os.path.splitext(filename)[0]  # 'argaba_100_0.1_5_5_3'
    # # Remove 'arg' prefix if present
    # if filename_wo_ext.startswith('arg'):
    #     instance_name = filename_wo_ext[3:]
    # else:
    #     instance_name = filename_wo_ext

    # #original_instance = "/Users/andrei/Documents/GitLab/discover-aba/running_example/running_example.lp"
    # original_instance = "/Users/andrei/Documents/GitLab/discover-aba/InstanceGenerator/benchmarks100"+"/"+instance_name+".lp"
    # get content of original instance-------------
    assumptions = []
    atoms = []
    rules = []

    with open(original_instance, 'r') as file:
        asp_instance = file.readlines()

    for line in asp_instance:
        line = line.strip()
        line = line.replace(' ', '')

        if line.startswith('assumption('):
            num = str(line[len('assumption('):-2])
            assumptions.append(num)
        elif line.startswith('atom('):
            num = str(line[len('atom('):-2])
            atoms.append(num)
        elif line.startswith('rule('):
            num = line[len('rule('):-2]
            rules.append(num)

    print("Assumptions:", assumptions)
    print("Atoms:", atoms)
    #print("Rules: ",rules)


    #----------------------------------------------
    # get arguments built for that instance--------
    constructed_arguments = []
    #print(sys.argv[1])
    # with open(sys.argv[1], 'r') as file:
    #     #dont include description in first line
    #     lines = file.readlines()
    with open(os.path.join(input_folder, filename), 'r') as file:
        #dont include description in first line
        lines = file.readlines()
    # for line in lines:
    #     line = line.replace(' ', '')
    #     arg = ast.literal_eval(line)
    #     constructed_arguments.append(arg)

    #select up to 10 arguments

    if len(lines) > 10:
        selected_lines = random.sample(lines, 10)
    else:
        selected_lines = lines

    #selected_lines = random.sample(lines, min(10, len(lines)))
    for line in selected_lines:
        line = line.replace(' ', '')
        arg = ast.literal_eval(line)
        if not arg in constructed_arguments:
            constructed_arguments.append(arg)
    #     if random.choice([True]*3 + [False]*7): #toss biased coin to decide whether to keep a rule or not
    #----------------------------------------------

    args = []
    arg_preds = []
    conclusion_preds = []
    assumption_preds = []
    pool_atm_preds=[]
    atom_preds = []
    rule_preds = []
    head_preds = []
    body_preds = []
    in_argument = []  # each entry: (argument_name, atom_included)
    related_preds = []



    related_preds_random = []


    # Random topic assignment
    # fix 10 topics
    topics = ["t1","t2","t3","t4","t5","t6","t7","t8","t9","t10"]
    allatoms = assumptions+atoms
    atom_to_topic = {atom: random.choice(topics) for atom in allatoms}
    # End random topic assignment------------------



    #Rule based topic assignment
    atoms_with_topic = []
    topic_count = 0
    seen_rules = []
    #--------------------------


    arg_names_count = {}

    for arg in constructed_arguments:

        conclusion = str(arg[2][0][0])

        if conclusion not in arg_names_count.keys(): #if this arg name is not taken
            arg_names_count[conclusion] = 0 #initialise with count 0
        else:
            arg_names_count[conclusion] = arg_names_count[conclusion] + 1
        


        print("Rule preds: ", rule_preds)

        arg_name = "arg"+conclusion+str(arg_names_count[conclusion])
        #arg_preds.append("argument("+"arg"+conclusion+").")

        arg_preds.append("argument("+arg_name+").")

        conclusion_preds.append("conclusion("+conclusion+","+arg_name+").")

        in_argument.append("inarg("+conclusion+","+str(arg_name)+").")
        atom_preds.append("atom("+conclusion+").")

        print("arg: ", arg, " - ", arg_name)

        #Rule based topic assignment
        topics = []
        related_arg_t = []
        #---------------------------


        # random based topic predicates
        for atom in arg[0][0]:
            related_preds_random.append("related("+atom_to_topic[str(atom)]+","+str(atom)+").")
        #----------------------------------


        for rule in arg[1][0]:
            

            #Rule based topic assignment
            if str(rule) not in seen_rules:
                seen_rules.append(str(rule))
                topic_count+=1

            topic = "t"+str(topic_count)
            #-------------------------------

            include = random.choice([True, False])
            print("rule: ",rule)

        
            if include == True:
                rule_preds.append("rule("+str(rule)+","+str(arg_name)+").")

            
                for line in asp_instance:
                    
                    if "head(" in line:

                        line = line.strip()  # remove any trailing \n or spaces
                        line = line.replace(' ', '')

                        
                        content = line[5:-2]  # remove 'head(' from start and ').' from end
                        parts = [x.strip() for x in content.split(',')]

                        
                        if parts and parts[0] == rule:
                            head_preds.append(line)
                            if "atom("+str(parts[1])+")." not in atom_preds:
                                atom_preds.append("atom("+str(parts[1])+").")
                            if "inarg("+str(parts[1])+","+str(arg_name)+")." not in in_argument:
                                in_argument.append("inarg("+str(parts[1])+","+str(arg_name)+").")
                        
                        
                            #add atom predicate, and in argument. Flat so can only be an atom
                    if line.startswith("body("):
                        # content = line[5:-1]  # Remove 'head(' and ')' at the ends
                        # parts = [x.strip() for x in content.split(',')]
                        line = line.strip()  # remove any trailing \n or spaces
                        line = line.replace(' ', '')
                        content = line[5:-2]  # remove 'head(' from start and ').' from end
                        parts = [x.strip() for x in content.split(',')]

                        if parts and parts[0] == rule:
                            body_preds.append(line)


                            #Rule based topic assignment
                            if str(parts[1]) not in atoms_with_topic:
                                related_preds.append("related("+topic+","+str(parts[1])+").")
                                atoms_with_topic.append(str(parts[1]))
                            #-----------------------------

                            if str(parts[1]) in assumptions:
                                assumption_preds.append("assumption("+str(parts[1])+").")
                            else:
                                if "atom("+str(parts[1])+")." not in atom_preds:
                                    atom_preds.append("atom("+str(parts[1])+").")
                            
                            if "inarg("+str(parts[1])+","+str(arg_name)+")." not in in_argument:
                                in_argument.append("inarg("+str(parts[1])+","+str(arg_name)+").")
            
            
            elif include == False:
                
                for line in asp_instance:
                    if line.startswith("head("):
                        line = line.strip()  # remove any trailing \n or spaces
                        line = line.replace(' ', '')

                        content = line[5:-2]  # remove 'head(' from start and ').' from end
                        parts = [x.strip() for x in content.split(',')]

                        if parts and parts[0] == rule:

                            if not "pool_atm("+str(parts[1])+")." in pool_atm_preds:
                                pool_atm_preds.append("pool_atm("+str(parts[1])+").")

                    if line.startswith("body("):
                
                        line = line.strip()  # remove any trailing \n or spaces
                        line = line.replace(' ', '')

                        content = line[5:-2]  # remove 'head(' from start and ').' from end
                        parts = [x.strip() for x in content.split(',')]

                        if parts and parts[0] == rule:

                            #Rule based topic assignment
                            if str(parts[1]) not in atoms_with_topic:
                                related_preds.append("related("+topic+","+str(parts[1])+").")
                                atoms_with_topic.append(str(parts[1]))
                            #---------------------------------------

                            if not str(parts[1]) in assumptions:
                                    if not "pool_atm("+str(parts[1])+")." in pool_atm_preds:
                                        pool_atm_preds.append("pool_atm("+str(parts[1])+").")
                            if str(parts[1]) in assumptions:
                                if not "pool_asm("+str(parts[1])+")." in pool_atm_preds:
                                    pool_atm_preds.append("pool_asm("+str(parts[1])+").")


    print("in argument: ", in_argument)
    print("assumptions: ", assumption_preds)
    print("atom rpeds: ", atom_preds)

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(output_dir_random, exist_ok=True)
    os.makedirs(output_dir_constructed, exist_ok=True)


    lp_output_path = os.path.join(output_dir, filename) #the instance of we got from those 10 arguments and by erasing things
    lp_output_path_random = os.path.join(output_dir_random, filename) #the instance of we got from those 10 arguments and by erasing things

    ca_output_path = os.path.join(output_dir_constructed, filename) #a file with the 10 selected arguments per instance

    with open(lp_output_path, 'w') as f:

        for pred in (
            arg_preds + conclusion_preds + assumption_preds +
            atom_preds + pool_atm_preds + in_argument +
            rule_preds + head_preds + body_preds + related_preds
        ):
            f.write(pred + "\n")
    
    with open(lp_output_path_random, 'w') as f:
        for pred in (
            arg_preds + conclusion_preds + assumption_preds +
            atom_preds + pool_atm_preds + in_argument +
            rule_preds + head_preds + body_preds + related_preds_random
        ):
            f.write(pred + "\n")
    
    with open(ca_output_path, 'w') as f:
        for arg in constructed_arguments:
            f.write(str(arg)+"\n")


