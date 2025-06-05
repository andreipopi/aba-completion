import os
import re

def extract_and_compile_results(input_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Traverse each subfolder in the input folder
    for solver in sorted(os.listdir(input_folder)):  # Sort the solver directories
        solver_path = os.path.join(input_folder, solver)

        results = []

        # Continue only if it is a directory
        if os.path.isdir(solver_path):
            output_subfolder = os.path.join(output_folder, solver)
            # Create subfolder in output directory
            if not os.path.exists(output_subfolder):
                os.makedirs(output_subfolder)

            # File to write the compiled results
            output_file_path = os.path.join(output_subfolder, f"{solver}_results.txt")
            with open(output_file_path, 'w') as output_file:
                # Sort files alphabetically before processing
                for file_name in sorted(os.listdir(solver_path)):
                    if file_name.endswith('.log'):
                        file_path = os.path.join(solver_path, file_name)

                        try:
                            # Read from the log file
                            with open(file_path, 'r') as file:
                                lines = file.readlines()
                                error_lines = [line.strip() for line in lines if 'ERROR' in line]

                                result_lines = [line.strip() for line in lines if 'OPTIMUM FOUND' in line or 'UNSATISFIABLE' in line]
                                timeout_lines = [line.strip() for line in lines if 'Maximum CPU time exceeded' in line] 
                                memoryout_lines = [line.strip() for line in lines if 'Maximum VSize exceeded' in line] 
                                models_lines = [line.strip() for line in lines if 'Models' in line] 
                                user_time_milliseconds = [line.strip() for line in lines if 'total CPU user time (s)' in line] 

                                instance_name = file_name.replace('.clingo.log', '')

                                # Extract the optimal answer set if present
                                answer_blocks = []
                                current_answer = []
                                in_answer = False
                                for line in lines:
                                    if line.strip().startswith('Answer:'):
                                        if in_answer:
                                            answer_blocks.append(' '.join(current_answer).strip())
                                        current_answer = []
                                        in_answer = True
                                    elif in_answer:
                                        if line.strip() == '' or line.strip().startswith(('Optimization:', 'OPTIMUM FOUND')):
                                            if current_answer:
                                                answer_blocks.append(' '.join(current_answer).strip())
                                            in_answer = False
                                        else:
                                            current_answer.append(line.strip())
                                if in_answer and current_answer:
                                    answer_blocks.append(' '.join(current_answer).strip())

                                optimal_answer = answer_blocks[-1] if answer_blocks else 'NO ANSWER'

                                if result_lines and not error_lines:
                                    last_result_line = result_lines[-1]
                                    results.append((instance_name, f"{instance_name}, {solver}, {last_result_line}, {user_time_milliseconds[0] if user_time_milliseconds else 'NO CPU TIME'}, {optimal_answer}\n"))

                                elif models_lines and timeout_lines == [] and memoryout_lines == []:
                                    last_result_line = models_lines[-1]
                                    results.append((instance_name, f"{instance_name}, {solver}, {last_result_line}, {user_time_milliseconds[0] if user_time_milliseconds else 'NO CPU TIME'}\n"))

                                elif error_lines != [] and timeout_lines == [] and memoryout_lines == []:
                                    results.append((instance_name, f"{instance_name}, {solver}, ERROR\n"))

                                elif timeout_lines != []:
                                    results.append((instance_name, f"{instance_name}, {solver}, TIMEOUT\n"))

                                elif memoryout_lines != []:
                                    results.append((instance_name, f"{instance_name}, {solver}, MEMORYOUT\n"))

                        except Exception as e:
                            print(f"Error processing file {file_path}: {e}")

        # Sort results by instance name
        results.sort(key=lambda x: x[0])

        # Write sorted results to file
        with open(output_file_path, 'w') as output_file:
            for _, line in results:
                output_file.write(line)

# Set your paths
input_folder = '/Users/andreipopi/Documents/GitLab/discover-aba/Experiments/results100_prefrand-run2'
output_folder = 'compiled_results_100_prefrand-run2'

# Call the function
extract_and_compile_results(input_folder, output_folder)