import os
import argparse

from HATracking.parse_ADL import interpolate_MOT
from HATracking.parse_ADL import *  # fix this

WRITE_OUT_GTS = False
# I'm not sure what this is
PRED_IN = "data/ADL/outputs/experiments/first_run_no_shift/preds"
GT_OUTPUT_FOLDER = "data/ADL/annotations/MOT_style"

ADL_OBJECT_ANNOTATIONS_FOLDER = "data/ADL/annotations/object_annotation"
ADL_FILE_FORMAT = "object_annot_P_{:02d}.txt"
GT_FORMAT = "P_{:02d}/gt/"

REMOVE_IMOVABLE = True

if REMOVE_IMOVABLE:
    PRED_OUT = "{}_filtered_movable".format(PRED_IN)
else:
    PRED_OUT = "{}_filtered".format(PRED_IN)

# make the output directory


def parse_args():
    """parse."""
    parser = argparse.ArgumentParser(
        "This is a testing environment for the hand aware tracking")
    parser.add_argument("--start", type=int,
                        help="which video to start at", default=1)
    parser.add_argument("--stop", type=int,
                        help="which video to end at, exclusive", default=21)
    parser.add_argument("--annotation-folder", type=str,
                        help="where to find the ADL annotations",
                        default=ADL_OBJECT_ANNOTATIONS_FOLDER)
    parser.add_argument("--output-folder", type=str,
                        help="Where to write out the reformated annotations",
                        default=GT_OUTPUT_FOLDER)
    parser.add_argument("--interpolate", type=str,
                        help="The type of interpoltation, 'linear' or 'cubic'. If not specified, no interpolation will be performed",
                        default=None)
    parser.add_argument("--remove-imovable", action="store_true",
                        help="Remove objects which cannot be moved. Currently DOES NOTHING")

    return parser.parse_args()


args = parse_args()

# iterate over all of the files
for i in range(args.start, args.stop):
    gt_input_file = os.path.join(args.annotation_folder,
                                 ADL_FILE_FORMAT.format(i))
    # TODO figure out what this is doing
    #pred_in_file = "{}/P_{:02d}.txt".format(PRED_IN, i)
    #pred = load_MOT(pred_in_file)
    # if REMOVE_IMOVABLE:
    #    ADL_gt = load_ADL(GT_IN)
    #    gt, pred = remove_imovable_objects(ADL_gt, pred)# TODO filter these again to get only the ones which line up
    # else:
    gt = ADL_to_MOT(load_ADL(gt_input_file))
    if args.interpolate is not None:
        gt = interpolate_MOT(gt, method=args.interpolate)
    #filtered_pred = remove_intermediate_frames(gt, pred)
    #filtered_pred.to_csv(os.path.join(PRED_OUT, "P_{:02d}.txt".format(i)), sep=" ", header=False, index=False)
    gt_output_folder = os.path.join(
        args.output_folder, GT_FORMAT.format(i))
    if not os.path.isdir(gt_output_folder):
        os.system("mkdir -p {}".format(gt_output_folder))
    gt_file = os.path.join(gt_output_folder, "gt.txt")
    # don't write a header or index column
    gt.to_csv(gt_file, sep=" ", header=False, index=False)
