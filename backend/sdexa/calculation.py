"""Based on a script of Lorenz Birnbacher (lorenz.birnbacher@tum.de)"""
import math
import numpy as np
from backend.sdexa.Result import Result
from backend.sdexa.constants import *


def background_correction(image):
    """To be done"""
    return image


def calculate_epl(image, mu):
    mm_to_cm_inverse = 1/10  # 1/mm to 1/cm
    return image / (prefactor.value * mu.value) * mm_to_cm_inverse


def calculate_line_integral_water(mu_water_p, mu_water_c, photo_epl, compton_epl):
    return mu_water_p.value * density_h2o.value * photo_epl + mu_water_c.value * density_h2o.value * compton_epl


def calculate_line_integral_soft_tissue(mu_soft_tissue_p, mu_soft_tissue_c, photo_epl, compton_epl):
    return mu_soft_tissue_p.value * st_density.value * photo_epl + mu_soft_tissue_c.value * st_density.value \
           * compton_epl


def calculate_bone_density(image, mask, scatter, region_of_interest):
    """ Find soft tissue region for better data precision.
    The mask is not only needed for the aBMD, but is also used for the soft tissue area here.
    The soft tissue area should contain only soft tissue.
    Here, potential adaption to mask y-offset and width of soft tissue area.
    """
    image_corrected = background_correction(image)
    scatter_corrected = background_correction(scatter)
    photo_epl = calculate_epl(image_corrected, mu_p)
    compton_epl = calculate_epl(scatter_corrected, mu_c)
    p50 = calculate_line_integral_water(mu_water_50_p, mu_water_50_c, photo_epl, compton_epl)
    p200 = calculate_line_integral_water(mu_water_200_p, mu_water_200_c, photo_epl, compton_epl)
    p50_st = calculate_line_integral_soft_tissue(mu_soft_tissue_50_p, mu_soft_tissue_50_c, photo_epl, compton_epl)
    p200_st = calculate_line_integral_soft_tissue(mu_soft_tissue_200_p, mu_soft_tissue_200_c, photo_epl, compton_epl)
    x0, y0, dx, dy = region_of_interest
    r_st = np.mean(p50_st[x0:x0+dx, y0:y0+dy] / p200_st[x0:x0+dx, y0:y0+dy])
    bone = (-r_st * p200 + p50) / (mu_bone_50.value - mu_bone_200.value * r_st)
    bone_density_matrix = mask * bone
    calculation_values = bone_density_matrix[np.where(mask)]
    calculation_values = [0] if calculation_values.size == 0 else calculation_values
    bone_density_mean = np.nanmean(calculation_values)
    bone_density_std = np.nanstd(calculation_values)
    return Result(
        np.where(np.isnan(bone_density_matrix), np.zeros(bone_density_matrix.shape), bone_density_matrix),
        0 if math.isnan(bone_density_mean) else bone_density_mean,
        0 if math.isnan(bone_density_std) else bone_density_std
    )
