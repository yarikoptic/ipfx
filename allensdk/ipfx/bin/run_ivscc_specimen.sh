OUTPUT_DIR=/local1/ephys/ivscc/specimens
CELL=$1

CELL_DIR=$OUTPUT_DIR/$CELL
INPUT_JSON=$CELL_DIR/pipeline_input.json
OUTPUT_JSON=$CELL_DIR/pipeline_output.json
LOG_FILE=$CELL_DIR/log.txt

echo $CELL_DIR

mkdir -p $CELL_DIR

python generate_ivscc_pipeline_input.py $CELL $CELL_DIR
python run_pipeline.py --input_json $INPUT_JSON --output_json $OUTPUT_JSON --log_level DEBUG |& tee $LOG_FILE