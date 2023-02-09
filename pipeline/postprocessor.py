import os
from udon2 import Importer, transform, visual


def draw_dependency_trees(outputs_dir, stage_dir, outputs_file):
    """
    Draw Dependency Trees.

    :param outputs_dir: Outputs Directory.
    :param stage_dir: Stage Directory.
    :param outputs_file: Outputs File.
    """
    trees = Importer.from_conll_file(os.path.join(outputs_dir, stage_dir, outputs_file))
    for index, tree in enumerate(trees):
        visual.render_dep_tree(tree, os.path.join(outputs_dir, stage_dir, "DT_" + str(index) + ".svg"),
                               options={"include_upos": True, "include_xpos": True, "include_ids": True, "include_feats": False})
        # visual.render_tree(transform.to_pct(tree), os.path.join(outputs_dir, stage_dir, "PCT_" + str(index) + ".svg"))
        # visual.render_tree(transform.to_grct(tree), os.path.join(outputs_dir, stage_dir, "GRCT_" + str(index) + ".svg"))
        # visual.render_tree(transform.to_lct(tree), os.path.join(outputs_dir, stage_dir, "LCT_" + str(index) + ".svg"))
