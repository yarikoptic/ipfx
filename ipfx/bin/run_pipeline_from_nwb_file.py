import allensdk.core.json_utilities as ju
import sys
import os.path
from ipfx.bin.run_pipeline import run_pipeline
from ipfx.bin.generate_pipeline_input import generate_pipeline_input
import ipfx.logging_utils as lu
import argparse

INPUT_JSON = "pipeline_input.json"
OUTPUT_JSON = "pipeline_output.json"


def main():
    """
    Runs pipeline for the given nwb file
    Usage:
    python pipeline_from_nwb_file.py <input_nwb_file> <output_dir>

    """

    parser = argparse.ArgumentParser()
    parser.add_argument("input_nwb_file",type=str)
    parser.add_argument("output_dir",type=str)
    args = vars(parser.parse_args())
    output_dir = args["output_dir"]
    input_nwb_file = args["input_nwb_file"]

    input_nwb_file_basename = os.path.basename(input_nwb_file)
    cell_name = os.path.splitext(input_nwb_file_basename)[0]

    cell_dir = os.path.join(output_dir,cell_name)

    if not os.path.exists(cell_dir):
        os.makedirs(cell_dir)

    lu.configure_logger(cell_dir)

    input = generate_pipeline_input(cell_dir = cell_dir,
                                    input_nwb_file = input_nwb_file)

    input_json = os.path.join(cell_dir,INPUT_JSON)
    ju.write(input_json,input)

    #   reading back from disk
    input = ju.read(input_json)
    output = run_pipeline(input["input_nwb_file"],
                          input["output_nwb_file"],
                          input.get("stimulus_ontology_file", None),
                          input.get("qc_fig_dir",None),
                          input["qc_criteria"],
                          input["manual_sweep_states"])

    ju.write(os.path.join(cell_dir,OUTPUT_JSON), output)

if __name__ == "__main__":
    main()



