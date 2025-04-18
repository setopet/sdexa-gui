""" Based on a script of Lorenz Birnbacher (lorenz.birnbacher@tum.de)
    Credits to ttps://github.com/tschoonj/xraylib for some of the used constants"""
from backend.sdexa.Constant import Constant

prefactor = Constant("prefactor", 2954.6394, None, "Philips dual-layer CT prefactor")
mu_p = Constant("mu_p", .001832764, None, "Philips dual-layer CT prefactor")
mu_c = Constant("mu_c", 0.0173672, None, "Philips dual-layer CT prefactor")

density_h2o = Constant("density_h2o", 0.992, "g/cm3")
mu_water_50_p = Constant("mu_water_50_p", 2.725E-2, "cm2/g", "CS_Photo_CP('H2O',50)")
mu_water_50_c = Constant("mu_water_50_c", 1.9948E-1, "cm2/g", "CS_Compt_CP('H2O',50)+CS_Rayl_CP('H2O',50)")
mu_water_200_p = Constant("mu_water_200_p", 2.887E-4, "cm2/g", "CS_Photo_CP('H2O',200)")
mu_water_200_c = Constant("mu_water_200_c", 1.36283E-1, "cm2/g", "CS_Compt_CP('H2O',200)+CS_Rayl_CP('H2O',200)")
mu_calcium_50 = Constant("mu_calcium_50", 1.023E+0)
mu_calcium_200 = Constant("mu_calcium_200", 1.374E-1)
mu_bone_50 = Constant("mu_bone_50", 4.242E-1, "cm2/g")
mu_bone_200 = Constant("mu_bone_200", 1.309E-1, "cm2/g")
st_density = Constant("st_density", 1.0, None, "GetCompoundDataNISTByIndex(162)['density']")
mu_soft_tissue_50 = Constant("mu_soft_tissue_50", 2.264E-1, "cm2/g", "TISSUE, SOFT (ICRU-44)")
mu_soft_tissue_200 = Constant("mu_soft_tissue_200", 1.358E-1, "cm2/g", "TISSUE, SOFT (ICRU-44)")
mu_soft_tissue_50_p = Constant("mu_soft_tissue_50_p", 2.725E-2, "cm2/g", "CS_Photo_CP(st_name,50)")
mu_soft_tissue_50_c = Constant("mu_soft_tissue_50_c", 1.9948E-1, "cm2/g",
                               "CS_Compt_CP(st_name,50)+CS_Rayl_CP(st_name,50)")
mu_soft_tissue_200_p = Constant("mu_soft_tissue_200_p", 2.887E-4, "cm2/g", "CS_Photo_CP(st_name,200)")
mu_soft_tissue_200_c = Constant("mu_soft_tissue_200_c", 1.36283E-1, "cm2/g",
                                "CS_Compt_CP(st_name,200)+CS_Rayl_CP(st_name,200)")
mu_adipose_tissue_50 = Constant("mu_adipose_tissue_50", 2.120E-1, "cm2/g", "TISSUE, ADIPOSE (ICRU-44)")
mu_adipose_tissue_200 = Constant("mu_adipose_tissue_200", 1.364E-1, "cm2/g", "TISSUE, ADIPOSE (ICRU-44)")

