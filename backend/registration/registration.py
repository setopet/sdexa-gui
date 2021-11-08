import SimpleITK as siTk


def perform_registration(fixed_image_array, moving_image_array):
    fixed_image = siTk.GetImageFromArray(fixed_image_array)
    moving_image = siTk.GetImageFromArray(moving_image_array)
    parameter_map = siTk.GetDefaultParameterMap("translation")
    image_filter = siTk.ElastixImageFilter()
    image_filter.SetFixedImage(fixed_image)
    image_filter.SetMovingImage(moving_image)
    image_filter.SetParameterMap(parameter_map)
    registration_result = image_filter.Execute()
    return siTk.GetArrayFromImage(registration_result)
