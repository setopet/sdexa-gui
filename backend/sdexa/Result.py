"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""


class Result:
    def __init__(self, bone_density_matrix, bone_density_mean, bone_density_std):
        self.__bone_density_matrix = bone_density_matrix
        self.__bone_density_mean = bone_density_mean
        self.__bone_density_std = bone_density_std

    @property
    def bone_density_matrix(self):
        return self.__bone_density_matrix

    @property
    def bone_density_mean(self):
        return self.__bone_density_mean

    @property
    def bone_density_std(self):
        return self.__bone_density_std
