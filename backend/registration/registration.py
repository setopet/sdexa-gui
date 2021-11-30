"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
import SimpleITK as siTk


def perform_registration(fixed_image_array, moving_image_array, number_iterations):
    """:returns the moving image registered on the fixed image."""
    fixed_image = siTk.GetImageFromArray(fixed_image_array)
    moving_image = siTk.GetImageFromArray(moving_image_array)
    image_filter = siTk.ElastixImageFilter()
    image_filter.SetFixedImage(fixed_image)
    image_filter.SetMovingImage(moving_image)
    image_filter.LogToFileOff()
    image_filter.LogToConsoleOff()
    image_filter.SetParameter("MaximumNumberOfIterations", str(number_iterations))
    set_parameters(image_filter)
    return siTk.GetArrayFromImage(image_filter.Execute())


def set_parameters(image_filter):
    image_filter.SetParameter("Transform", "TranslationTransform")
    image_filter.SetParameter("AutomaticParameterEstimation", "true")
    image_filter.SetParameter("CheckNumberOfSamples", "true")
    image_filter.SetParameter("DefaultPixelValue", "0")
    image_filter.SetParameter("FinalBSplineInterpolationOrder", "2")
    image_filter.SetParameter("FixedImagePyramid", "FixedSmoothingImagePyramid")
    image_filter.SetParameter("FixedImagePyramidSchedule", "8 8 8 4 4 4 2 2 2 1 1 1")
    image_filter.SetParameter("ImageSampler", "RandomCoordinate")
    image_filter.SetParameter("Interpolator", "LinearInterpolator")
    image_filter.SetParameter("MaximumNumberOfSamplingAttempts", "4")
    image_filter.SetParameter("Metric", "AdvancedMattesMutualInformation")
    image_filter.SetParameter("MovingImagePyramid", "MovingSmoothingImagePyramid")
    image_filter.SetParameter("MovingImagePyramidSchedule", "8 8 8 4 4 4 2 2 2 1 1 1")
    image_filter.SetParameter("NewSamplesEveryIteration", "true")
    image_filter.SetParameter("NumberOfResolutions", "4")
    image_filter.SetParameter("NumberOfSamplesForExactGradient", "4096")
    image_filter.SetParameter("NumberOfSpatialSamples", "4096")
    image_filter.SetParameter("Optimizer", "AdaptiveStochasticGradientDescent")
    image_filter.SetParameter("Registration", "MultiResolutionRegistration")
    image_filter.SetParameter("ResampleInterpolator", "FinalBSplineInterpolator")
    image_filter.SetParameter("Resampler", "DefaultResampler")
    return image_filter
