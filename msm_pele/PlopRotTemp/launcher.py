import os
import msm_pele.constants as cs
import msm_pele.Helpers.helpers as hp

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess
except SyntaxError:
    import subprocess

def parametrize_miss_residues(args, env, syst, resname=None):
    resname = args.residue if not resname else resname
    SPYTHON = os.path.join(cs.SCHRODINGER, "utilities/python")
    if not os.path.exists(SPYTHON):
        SPYTHON = os.path.join(cs.SCHRODINGER, "run")
    file_path = os.path.abspath(os.path.join(cs.DIR, "PlopRotTemp/main.py"))
    options = retrieve_options(args, env)
    templatedir = os.path.join(env.pele_dir, "DataLocal/Templates/OPLS2005/HeteroAtoms")
    rotamerdir = os.path.join(env.pele_dir, "DataLocal/LigandRotamerLibs")  
    mae_cahrges = True if args.mae_lig else False
    print("Running Plop")
    print("{} {} {} {} --outputname {} --templatedir {} --rotamerdir {}".format(SPYTHON, file_path, options, syst.lig, resname, templatedir, rotamerdir))
    subprocess.call("{} {} {} {} --outputname {} --templatedir {} --rotamerdir {}".format(SPYTHON, file_path, options, syst.lig, resname, templatedir, rotamerdir).split())
    #hp.silentremove([syst.lig])


def retrieve_options(args, env):
    """
    Retrieve PlopRotTemp options from input arguments
    """

    options = []
    if args.core != -1:
        options.extend(["--core {}".format(args.core)])
    if args.mtor != 4:
        options.extend(["--mtor {}".format(args.mtor)])
    if args.n != 1000:
        options.extend(["--n {}".format(args.n)])
    if args.forcefield != "OPLS2005":
        options.extend(["--force {}".format(args.forcefield)])
    if args.mae_lig:
        options.extend(["--mae_charges"])
    if args.gridres != 10:
        options.extend(["--gridres {}".format(args.gridres)])
    return " ".join(options)

