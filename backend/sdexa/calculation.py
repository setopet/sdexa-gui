import numpy as np

from backend import normalize_array
from constants import *


def calibrate_areal_bone_mineral_density_mean(bone_density_mean):
    return bone_density_mean * bone_density_calibration_factor_a + bone_density_calibration_factor_b


def calibrate_bone_density_std(bone_density_std):
    return bone_density_std * bone_density_calibration_factor_a


def background_correction(image):
    return image


def calculate_epl(image, mu):
    return image / (prepfactor.value * mu.value) * 0.1


def calculate_line_integral_water(mu_water_p, mu_water_c, photo_epl, compton_epl):
    return mu_water_p.value * density_h2o.value * photo_epl + mu_water_c.value * density_h2o.value * compton_epl


def calculate_line_integral_soft_tissue(mu_soft_tissue_p, mu_soft_tissue_c, photo_epl, compton_epl):
    return mu_soft_tissue_p.value * st_density.value * photo_epl + mu_soft_tissue_c * st_density.value * compton_epl


def apply_mask(image, mask, scatter):
    """ Find soft tissue region for better data precision.
    The mask is not only needed for the aBMD, but is also used for the soft tissue area here.
    The soft tissue area should contain only soft tissue.
    Here, potential adaption to mask y-offset and width of soft tissue area.
    """
    image = background_correction(image)
    mask = background_correction(mask)
    scatter = background_correction(scatter)

    photo_epl = calculate_epl(image, mu_p)
    compton_epl = calculate_epl(scatter, mu_c)
    p50 = calculate_line_integral_water(mu_water_50_p, mu_water_50_c, photo_epl, compton_epl)
    p200 = calculate_line_integral_water(mu_water_200_p, mu_water_200_c, photo_epl, compton_epl)
    p50_st = calculate_line_integral_soft_tissue(mu_soft_tissue_50_p, mu_soft_tissue_50_c, photo_epl, compton_epl)
    p200_st = calculate_line_integral_soft_tissue(mu_soft_tissue_200_p, mu_soft_tissue_200_c, photo_epl, compton_epl)

    roi = 0, 1, 0, 1  # Selection rectangle of soft tissue in GUI
    x0, x, y0, y = roi
    r_st = np.mean(p50_st[x0:x, y0:y] / p200_st[x0:x, y0:y])
    bone = (-r_st * p200 + p50) / (mu_bone_50 - mu_bone_200 * r_st)
    # problem with different regions, vertebral bodies should be differentiated.
    tmp = np.zeros_like(mask)
    tmp[x0:x, y0:y] = np.max(bone)

    marked = normalize_array(bone + tmp, 1)
    aBMD = mask * bone  # + _tmp
    aBMD_mean = np.mean(bone[np.where(mask > 0.5)])
    aBMD_std = np.std(bone[np.where(mask > 0.5)])

    