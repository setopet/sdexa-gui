


def background_correction(self, bg_path):
    self.bg_path = bg_path
    """Not yet used"""
    try:
        background_compton = scipy.io.loadmat(self.bg_path + self.load_string + '_compton.mat')['img2']
        background_photo = scipy.io.loadmat(self.bg_path + self.load_string + '_photo.mat')['img']
        self.compton_raw -= background_compton[:, self.offset:self.compton_raw.shape[1] + self.offset]
        self.photo_raw -= self.photo_raw - background_photo[:, self.offset:self.photo_raw.shape[1] + self.offset]
    except:
        print('Background correction not available')


def calculate_epl(self):
    # Change the raw philips detector data to the water equivalent path length
    # This means our data is comprised of x cm water Compton and y cm water photoeffect.
    self.compton_epl = self.compton_raw / (prepfactor * mu_c)
    self.photo_epl = self.photo_raw / (prepfactor * mu_p)

    # Change the units from 1/mm to 1/cm
    self.compton_epl *= 0.1  # mm to cm
    self.photo_epl *= 0.1  # mm to cm


def calculate_line_integral_water(self):
    # Now we calculate the estimated monoenergetic line integral P for two energies 50 and 200 keV
    # p is without unit
    # The line integrals represent the combination of photo and compton cross sections
    self.p50 = mu_water_50_p * density_h2o * self.photo_epl + mu_water_50_c * density_h2o * self.compton_epl
    self.p200 = mu_water_200_p * density_h2o * self.photo_epl + mu_water_200_c * density_h2o * self.compton_epl


def calculate_line_integral_soft_tissue(self):
    # Now we calculate the estimated monoenergetic line integral P for two energies 50 and 200 keV
    # p is without unit
    # The line integrals represent the combination of photo and compton cross sections
    self.p50_st = mu_soft_tissue_50_p * st_density * self.photo_epl + mu_soft_tissue_50_c * st_density * self.compton_epl  # -0.26 m
    self.p200_st = mu_soft_tissue_200_p * st_density * self.photo_epl + mu_soft_tissue_200_c * st_density * self.compton_epl  # -.15


def apply_mask(self, mask_path):
    self.mask_path = mask_path
    # do stuff
    ### Find soft tissue region for better data precision
    mask_path_name = self.mask_path
    mask = np.load(mask_path_name + "_output-photo_r2.npy").astype(np.float32)[0]

    '''
    The mask is not only needed for the aBMD, but is also used for the soft tissue area here. 
    The soft tissue area shold contain only soft tissue. 
    Here, potential adaption to mask y-offset and width of soft tissue area. 
    '''
    y, x = cal_center_of_mass(mask)

    # roi = mask[y-offset_y - width:y-offset_y,x-offset_x-width//2:x-offset_x+width//2]
    self.roi = (
    y - self.roi_offset_y - self.roi_width, y - self.roi_offset_y, x - self.roi_offset_x - self.roi_width // 2,
    x - self.roi_offset_x + self.roi_width // 2)

    self.calculate_line_integral_soft_tissue()
    self.R_st = np.mean(
        self.p50_st[self.roi[0]:self.roi[1], self.roi[2]:self.roi[3]] / self.p200_st[self.roi[0]:self.roi[1],
                                                                        self.roi[2]:self.roi[3]])

    # R_ca = mu_soft_tissue_50/mu_soft_tissue_200
    self.bone = (-self.R_st * self.p200 + self.p50) / (mu_bone_50 - mu_bone_200 * self.R_st)

    # problem with different regions, vertebral bodies should be differentiated.
    _tmp = np.zeros_like(mask)
    _tmp[self.roi[0]:self.roi[1], self.roi[2]:self.roi[3]] = np.max(self.bone)
    self.marked = normalize(self.bone + _tmp)
    self.aBMD = mask * self.bone  # + _tmp
    self.aBMD_mean = np.mean(self.bone[np.where(mask > 0.5)])
    self.aBMD_std = np.std(self.bone[np.where(mask > 0.5)])

    # Calibrate BMD: (values by prior work, have to be checked. are determined without background correction)
    # Too many wild calibrations
    a_cal = 1.0745
    b_cal = 0.1359
    self.aBMD_corr = self.aBMD_mean * a_cal + b_cal
    self.aBMD_std_corr = self.aBMD_std * a_cal


def calculate_bone(self):
    self.R_st = mu_soft_tissue_50 / mu_soft_tissue_200
    # This value is too off theoretically and an experimental value should be used
    # Masks are good to use here.

    self.bone = (-self.R_st * self.p200 + self.p50) / (mu_bone_50 - mu_bone_200 * self.R_st)


def calculate_soft_tissue(self):
    self.R_bone = mu_bone_50 / mu_bone_200
    # This value is too off theoretically and an experimental value should be used
    # Masks are good to use here.

    self.soft_tissue = (-self.R_bone * self.p200 + self.p50) / (mu_soft_tissue_50 - mu_soft_tissue_200 * self.R_bone)
