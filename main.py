import Dr_Maxworth_model as pfi
import lorentzforce_p_sim as lfps

import particles as pts


if __name__ == "__main__":
    # pfi.main(particle_type="proton", case="2")
    lfps.main(pts.SimpleParticle)
    lfps.main(pts.PosComputeParticle)
