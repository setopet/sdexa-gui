import SimpleITK as siTk


def perform_registration(fixed_image_array, moving_image_array):
    """:returns the moving image registered on the fixed image."""
    fixed_image = siTk.GetImageFromArray(fixed_image_array)
    moving_image = siTk.GetImageFromArray(moving_image_array)
    parameter_map = siTk.GetDefaultParameterMap("translation")
    image_filter = siTk.ElastixImageFilter()
    image_filter.LogToConsoleOff()
    image_filter.LogToFileOff()
    image_filter.SetFixedImage(fixed_image)
    image_filter.SetMovingImage(moving_image)
    image_filter.SetParameterMap(parameter_map)
    return siTk.GetArrayFromImage(image_filter.Execute())
