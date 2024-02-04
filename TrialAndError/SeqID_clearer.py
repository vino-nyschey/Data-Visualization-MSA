import os

def process_fasta(input_file, output_file):
    with open(input_file, 'r') as f_in:
        with open(output_file, 'w') as f_out:
            for line in f_in:
                if line.startswith('>'):  # Head
                    header = line.split(' ', 1)[0] + '\n'
                    f_out.write(header)
                else:
                    f_out.write(line)

if __name__ == "__main__":
    input_folder = "fasta_files//MSA_align_files"
    output_folder = "fasta_files//MSA_align_files_header_cleared"


    for filename in os.listdir(input_folder):
        if filename.endswith('.fasta'):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename.split('.')[0] + '_modified.fasta')

            process_fasta(input_file, output_file)
            print(f"Processed {input_file} -> {output_file}")

    print("DONE")
