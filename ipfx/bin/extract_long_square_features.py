from ipfx.data_set_utils import create_data_set
import ipfx.data_set_features as dsf
import ipfx.stim_features as stf
import ipfx.stimulus_protocol_analysis as spa
from ipfx.stimulus import StimulusOntology
import allensdk.core.json_utilities as ju


def main():

    nwb_file_full_path ="/local1/ephys/nwb2/MIES/Vip-IRES-Cre;Ai14-331294.04.01.01-compressed.nwb"
    stimulus_ontology_file = StimulusOntology.DEFAULT_STIMULUS_ONTOLOGY_FILE

    ontology = StimulusOntology(ju.read(stimulus_ontology_file))

    data_set = create_data_set(nwb_file=nwb_file_full_path, ontology=ontology)

    lsq_sweep_numbers = data_set.filtered_sweep_table(clamp_mode=data_set.CURRENT_CLAMP,
                                                      stimuli=ontology.long_square_names).sweep_number.sort_values().values

    lsq_sweeps = data_set.sweep_set(lsq_sweep_numbers)
    lsq_sweeps.select_epoch("recording")
    lsq_sweeps.align_to_start_of_epoch("experiment")
    lsq_start, lsq_dur, _, _, _ = stf.get_stim_characteristics(lsq_sweeps.sweeps[0].i,
                                                               lsq_sweeps.sweeps[0].t)

    lsq_end = lsq_start + lsq_dur
    lsq_spx, lsq_spfx = dsf.extractors_for_sweeps(lsq_sweeps,
                                                  start=lsq_start,
                                                  end=lsq_end,
                                                  **dsf.detection_parameters(data_set.LONG_SQUARE))

    lsq_an = spa.LongSquareAnalysis(lsq_spx, lsq_spfx, subthresh_min_amp=-100.)

    lsq_features = lsq_an.analyze(lsq_sweeps)

    return lsq_sweeps, lsq_features, lsq_start, lsq_end


if __name__=="__main__":

    main()
