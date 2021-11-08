import SimpleITK as siTk


def perform_registration(surview, ct_projection):
    surview_image = siTk.GetArrayFromImage(surview)
    ct_projection_image = siTk.GetImageFromArray(ct_projection)
    parameter_map = siTk.GetDefaultParameterMap("translation")
    image_filter = siTk.ElastixImageFilter()
    image_filter.SetFixedImage(surview_image)
    image_filter.SetMovingImage(ct_projection_image)
    image_filter.SetParameterMap(parameter_map)
    registration_result = image_filter.Execute()
    return siTk.GetArrayFromImage(registration_result)
