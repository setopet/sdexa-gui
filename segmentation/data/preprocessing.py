import numpy as np
import SimpleITK as sitk


def read_image(imagefile, mask=False):
    image = sitk.ReadImage(str(imagefile))

    if mask:
        image = _resample_img(image, mask=True)
    else:
        image = _resample_img(image)

    data = _reverse_axes(sitk.GetArrayFromImage(image))  # switch from zyx to xyz
    header = {
        'spacing': image.GetSpacing(),
        'origin': image.GetOrigin(),
        'direction': image.GetDirection()
    }

    return data, header


def preprocess_image(data, header, axis=1, mask=False, masks=[20, 21, 22, 23]):
    data, header = _normalize_slice_orientation(data, header)

    data = _window_image(data, 500, 1000)

    if mask:
        data = np.isin(data, masks).astype(np.int)

    data = np.rot90(data.sum(axis=axis))

    if mask:
        data[data < 30] = 0
        data[data >= 30] = 1

    data = _crop_image(data)

    data = _add_pad(data)

    data = _normalize_and_rescale(data)

    return data


def _normalize_and_rescale(image):
    return (image / image.max()) * 255


def _reverse_axes(image):
    return np.transpose(image, tuple(reversed(range(image.ndim))))


def _crop_image(image, new_height=512, new_width=512):
    height, width = image.shape

    y0 = (height - new_height) // 2 if height >= new_height else 0
    x0 = (width - new_width) // 2 if width >= new_width else 0

    return image[y0:y0+new_height, x0:x0+new_width]


def _add_pad(image, new_height=512, new_width=512):
    height, width = image.shape

    final_image = np.zeros((new_height, new_width))

    pad_left = int((new_width - width) / 2)
    pad_top = int((new_height - height) / 2)

    # Replace the pixels with the image's pixels
    final_image[pad_top:pad_top + height, pad_left:pad_left + width] = image

    return final_image


def _resample_img(image, out_spacing=[1.0, 1.0, 1.0], mask=False):
    # Resample images to 1mm spacing with SimpleITK
    original_spacing = image.GetSpacing()
    original_size = image.GetSize()

    out_size = [
        int(np.round(original_size[0] * (original_spacing[0] / out_spacing[0]))),
        int(np.round(original_size[1] * (original_spacing[1] / out_spacing[1]))),
        int(np.round(original_size[2] * (original_spacing[2] / out_spacing[2])))]

    resample = sitk.ResampleImageFilter()
    resample.SetOutputSpacing(out_spacing)
    resample.SetSize(out_size)
    resample.SetOutputDirection(image.GetDirection())
    resample.SetOutputOrigin(image.GetOrigin())
    resample.SetTransform(sitk.Transform())
    resample.SetDefaultPixelValue(image.GetPixelIDValue())

    if mask:
        resample.SetInterpolator(sitk.sitkNearestNeighbor)
    else:
        resample.SetInterpolator(sitk.sitkBSpline)

    return resample.Execute(image)

def _swap_flip_dimensions(cosine_matrix, image, header=None):
    # Compute swaps and flips
    swap = np.argmax(abs(cosine_matrix), axis=0)
    flip = np.sum(cosine_matrix, axis=0)

    # Apply transformation to image volume
    image = np.transpose(image, tuple(swap))
    image = image[tuple(slice(None, None, int(f)) for f in flip)]

    if header is None:
        return image

    # Apply transformation to header
    header['spacing'] = tuple(header['spacing'][s] for s in swap)
    header['direction'] = np.eye(3)

    return image, header


def _normalize_slice_orientation(image, header):
    # Preserve original header so that we can easily transform back
    header['original'] = header.copy()

    # Compute inverse of cosine (round first because we assume 0/1 values only)
    # to determine how the image has to be transposed and flipped for cosine = identity
    cosine = np.asarray(header['direction']).reshape(3, 3)
    cosine_inv = np.linalg.inv(np.round(cosine))

    return _swap_flip_dimensions(cosine_inv, image, header)


def _window_image(image, window_center, window_width):
    img_min = window_center - window_width // 2
    img_max = window_center + window_width // 2
    window_image = image.copy()
    window_image[window_image < img_min] = img_min
    window_image[window_image > img_max] = img_max

    return window_image