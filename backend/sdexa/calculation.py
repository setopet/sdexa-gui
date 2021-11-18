import numpy as np
from backend import normalize_array
from backend.sdexa.Result import Result
from constants import *


def calibrate_bone_density_mean(bone_density_mean):
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


# TODO: Entfernen, wenn man das nicht braucht
def get_marked_region(bone, mask_corrected, region_of_interest):
    x0, x, y0, y = region_of_interest
    array = np.zeros_like(mask_corrected)  # problem with different regions, vertebral bodies should be differentiated.
    array[x0:x, y0:y] = np.max(bone)
    return normalize_array(bone + array, 1)


def apply_mask(image, mask, scatter, region_of_interest):
    """ Find soft tissue region for better data precision.
    The mask is not only needed for the aBMD, but is also used for the soft tissue area here.
    The soft tissue area should contain only soft tissue.
    Here, potential adaption to mask y-offset and width of soft tissue area.
    """
    image_corrected = background_correction(image)
    mask_corrected = background_correction(mask)
    scatter_corrected = background_correction(scatter)
    photo_epl = calculate_epl(image_corrected, mu_p)
    compton_epl = calculate_epl(scatter_corrected, mu_c)
    p50 = calculate_line_integral_water(mu_water_50_p, mu_water_50_c, photo_epl, compton_epl)
    p200 = calculate_line_integral_water(mu_water_200_p, mu_water_200_c, photo_epl, compton_epl)
    p50_st = calculate_line_integral_soft_tissue(mu_soft_tissue_50_p, mu_soft_tissue_50_c, photo_epl, compton_epl)
    p200_st = calculate_line_integral_soft_tissue(mu_soft_tissue_200_p, mu_soft_tissue_200_c, photo_epl, compton_epl)
    x0, x, y0, y = region_of_interest
    r_st = np.mean(p50_st[x0:x, y0:y] / p200_st[x0:x, y0:y])
    bone = (-r_st * p200 + p50) / (mu_bone_50 - mu_bone_200 * r_st)
    bone_density_matrix = mask_corrected * bone
    bone_density_mean = np.mean(bone[np.where(mask_corrected > 0.5)])
    bone_density_std = np.std(bone[np.where(mask_corrected > 0.5)])
    return Result(
        bone_density_matrix,
        calibrate_bone_density_mean(bone_density_mean),
        calibrate_bone_density_std(bone_density_std))
