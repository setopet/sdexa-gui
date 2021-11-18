from backend.sdexa.Constant import Constant


CONSTANTS = {constant.name: constant.value for constant in [
        Constant("prepfactor", 2954.6394, None, "Philips dual-layer CT prefactor"),
        Constant("mu_p", .001832764, None, "Philips dual-layer CT prefactor"),
        Constant("mu_c", 0.0173672, None, "Philips dual-layer CT prefactor"),
        Constant("density_h2o", 0.992, "g/cm3"),
        Constant("mu_water_50_p", 2.725E-2, "cm2/g", "CS_Photo_CP('H2O',50)"),
        Constant("mu_water_50_c", 1.801E-1+1.938E-2, "cm2/g", "CS_Compt_CP('H2O',50)+CS_Rayl_CP('H2O',50)"),
        Constant("mu_water_200_p", 2.887E-4, "cm2/g", "CS_Photo_CP('H2O',200)"),
        Constant("mu_water_200_c", 1.349E-1+1.383E-3, "cm2/g", "CS_Compt_CP('H2O',200)+CS_Rayl_CP('H2O',200)"),
        Constant("mu_bone_50", 4.242E-1, "cm2/g"),
        Constant("mu_bone_200", 1.309E-1, "cm2/g"),
        Constant("mu_soft_tissue_50", 2.264E-1, "cm2/g", "TISSUE, SOFT (ICRU-44)"),
        Constant("mu_soft_tissue_200", 1.358E-1, "cm2/g", "TISSUE, SOFT (ICRU-44)"),
        # TODO: Werte von folgenden drei Konstanten:
        Constant("soft_tissue_data", None, None, "GetCompoundDataNISTByIndex(162)"),
        Constant("st_name", None, None, "soft_tissue_data['name']"),
        Constant("st_density", None, None, "soft_tissue_data['density']"),
        Constant("mu_soft_tissue_50_p", 2.725E-2, "cm2/g", "CS_Photo_CP(st_name,50)"),
        Constant("mu_soft_tissue_50_c", 1.801E-1+1.938E-2, "cm2/g", "CS_Compt_CP(st_name,50)+CS_Rayl_CP(st_name,50)"),
        Constant("mu_soft_tissue_200_p", 2.887E-4, "cm2/g", "CS_Photo_CP(st_name,200)"),
        Constant("mu_soft_tissue_200_c", 1.349E-1+1.383E-3, "cm2/g", "CS_Compt_CP(st_name,200)+CS_Rayl_CP(st_name,200)"),
        Constant("mu_adipose_tissue_50", 2.120E-1, "cm2/g", "TISSUE, ADIPOSE (ICRU-44)"),
        Constant("mu_adipose_tissue_200", 1.364E-1, "cm2/g", "TISSUE, ADIPOSE (ICRU-44)"),
        Constant("mu_calcium_50", 1.023E+0),
        Constant("mu_calcium_200", 1.374E-1)
    ]}

