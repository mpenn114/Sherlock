from typing import List, Tuple, Union

import numpy as np

from .config import EnvSettings

ENV = EnvSettings()


def animal_finder(image: np.ndarray, background_image: np.ndarray, is_daytime: bool):
    """
    Identify animals in an image by locating bounding rectangles around detected points.

    This function searches for potential animals within the provided image, then filters
    and merges overlapping bounding rectangles, returning the pruned coordinates of the
    detected areas.

    Args:
        image (np.ndarray): The image in which to detect animals.
        background_image (np.ndarray): The background image
        is_daytime (bool): Whether or not this image was a daytime image
    Returns:
        tuple: Pruned lists of left, right, bottom, and top coordinates for bounding rectangles.
    """
    left_bounds: List[int] = []
    right_bounds: List[int] = []
    top_bounds: List[int] = []
    bottom_bounds: List[int] = []

    new_positions, animal_count = animal_inner(image, background_image, is_daytime)

    for i in range(animal_count):
        position = new_positions[i]
        is_new_point = (
            np.sum(
                (left_bounds < position[0])
                * (right_bounds > position[0])
                * (top_bounds > position[1])
                * (bottom_bounds < position[1])
            )
            == 0
        )

        if is_new_point:
            left, right, top, bottom = bounce(
                image, background_image, is_daytime, position
            )

            if left < right and bottom < top:
                for _ in range(ENV.bounces):
                    x_position = np.random.randint(left, right)
                    y_position = np.random.randint(bottom, top)
                    left_new, right_new, top_new, bottom_new = bounce(
                        image,
                        background_image,
                        is_daytime,
                        np.array([x_position, y_position]),
                    )
                    left = min(left, left_new)
                    right = max(right, right_new)
                    top = max(top, top_new)
                    bottom = min(bottom, bottom_new)

                left_bounds.append(left)
                right_bounds.append(right)
                top_bounds.append(top)
                bottom_bounds.append(bottom)

    prune_count = 0
    pruned_lefts: List[int] = []
    pruned_rights: List[int] = []
    pruned_tops: List[int] = []
    pruned_bottoms: List[int] = []

    for i in range(len(left_bounds)):
        overlapped_index = -1
        for j in range(prune_count):
            if (
                overlap(
                    left_bounds[i],
                    right_bounds[i],
                    top_bounds[i],
                    bottom_bounds[i],
                    pruned_lefts[j],
                    pruned_rights[j],
                    pruned_tops[j],
                    pruned_bottoms[j],
                )
                > 0
            ):
                overlapped_index = j
                break

        if overlapped_index == -1:
            pruned_lefts.append(left_bounds[i])
            pruned_rights.append(right_bounds[i])
            pruned_bottoms.append(bottom_bounds[i])
            pruned_tops.append(top_bounds[i])
            prune_count += 1
        else:
            pruned_lefts[overlapped_index] = min(
                left_bounds[i], pruned_lefts[overlapped_index]
            )
            pruned_rights[overlapped_index] = max(
                right_bounds[i], pruned_rights[overlapped_index]
            )
            pruned_tops[overlapped_index] = max(
                top_bounds[i], pruned_tops[overlapped_index]
            )
            pruned_bottoms[overlapped_index] = min(
                bottom_bounds[i], pruned_bottoms[overlapped_index]
            )

    carryover_x_positions = np.zeros((prune_count, 1))
    carryover_y_positions = np.zeros((prune_count, 1))

    for i in range(prune_count):
        carryover_x_positions[i] = round(0.5 * (pruned_lefts[i] + pruned_rights[i]))
        carryover_y_positions[i] = round(0.5 * (pruned_tops[i] + pruned_bottoms[i]))

    return pruned_lefts, pruned_rights, pruned_bottoms, pruned_tops


def animal_inner(
    image: np.ndarray, background_image: np.ndarray, is_daytime: bool
) -> Tuple[np.ndarray, int]:
    """
    Identify potential animal positions in an image by comparing sampled pixels with a background image.

    This function samples pixels from the input image and background image, calculates differences,
    and filters based on color and greyscale criteria to detect areas that could contain animals.

    Args:
        image (np.ndarray): The input image to analyze.
        background_image (np.ndarray): Background reference image for comparison.
        is_daytime (bool): Flag indicating whether it's daytime, which affects tolerance values.

    Returns:
        tuple: Array of identified positions and the count of potential animals.
    """
    background_tolerance = (
        ENV.background_tol_day if is_daytime else ENV.background_tol_night
    )
    image_shape = image.shape

    x_samples = np.random.randint(0, image_shape[1] - 1, size=ENV.sample_size)
    y_samples = np.random.randint(0, image_shape[0] - 1, size=ENV.sample_size)

    image_samples = image[y_samples, x_samples].astype(int)
    background_samples = background_image[y_samples, x_samples].astype(int)
    diff_samples = np.abs(background_samples - image_samples).astype(int)

    valid_samples = (
        (
            np.max(image_samples, axis=1) - np.min(image_samples, axis=1)
            < ENV.greyscale_parameter
        )
        & (np.max(diff_samples, axis=1) > background_tolerance)
        & (np.sum(image_samples < ENV.colour_upper, axis=1) == 3)
        & (np.sum(image_samples > ENV.colour_lower, axis=1) == 3)
    )

    positions = np.zeros((len(x_samples[valid_samples]), 2))
    positions[:, 1] = x_samples[valid_samples]
    positions[:, 0] = y_samples[valid_samples]
    animal_count = len(positions)

    return positions, animal_count


def bounce(
    image: np.ndarray,
    background_image: np.ndarray,
    is_daytime: bool,
    position: np.ndarray,
) -> Tuple[int, int, int, int]:
    """
    Calculate the bounding coordinates of an object as it "bounces" within an image.

    The function attempts to move an object in each cardinal direction (up, down, left, right),
    constrained by a specified background tolerance level. The movement stops when no further
    displacement is possible in a given direction.

    Args:
        image (np.ndarray): The image containing the object.
        background_image (np.ndarray): The background image for comparison.
        is_daytime (bool): Flag indicating if daytime background tolerance should be used.
        position (np.ndarray): Initial position of the object as a 2D array.

    Returns:
        Tuple[float, float, float, float]: Bounding coordinates in the order (left, right, top, bottom).
    """
    initial_position = position.copy()

    left_bound, right_bound = position[0], position[0]
    top_bound, bottom_bound = position[1], position[1]

    # Attempt to move upwards
    while True:
        position, movement = directional_walk(
            image,
            background_image,
            is_daytime,
            np.array([0.0, 1.0]),
            position,
        )
        if movement == 0:
            position, movement = directional_walk(
                image,
                background_image,
                is_daytime,
                np.array([-1.0, 1.0]),
                position,
            )
            if movement == 0:
                position, movement = directional_walk(
                    image,
                    background_image,
                    is_daytime,
                    np.array([1.0, 1.0]),
                    position,
                )
        top_bound = max(position[1], top_bound)
        left_bound = min(position[0], left_bound)
        right_bound = max(position[0], right_bound)
        if movement == 0:
            break

    # Reset position and attempt to move downwards
    position = initial_position.copy()
    while True:
        position, movement = directional_walk(
            image,
            background_image,
            is_daytime,
            np.array([0.0, -1.0]),
            position,
        )
        if movement == 0:
            position, movement = directional_walk(
                image,
                background_image,
                is_daytime,
                np.array([1.0, -1.0]),
                position,
            )
            if movement == 0:
                position, movement = directional_walk(
                    image,
                    background_image,
                    is_daytime,
                    np.array([-1.0, -1.0]),
                    position,
                )
        bottom_bound = min(position[1], bottom_bound)
        left_bound = min(position[0], left_bound)
        right_bound = max(position[0], right_bound)
        if movement == 0:
            break

    # Reset position and attempt to move leftwards
    position = initial_position.copy()
    while True:
        position, movement = directional_walk(
            image,
            background_image,
            is_daytime,
            np.array([-1.0, 0.0]),
            position,
        )
        if movement == 0:
            position, movement = directional_walk(
                image,
                background_image,
                is_daytime,
                np.array([-1.0, -1.0]),
                position,
            )
            if movement == 0:
                position, movement = directional_walk(
                    image,
                    background_image,
                    is_daytime,
                    np.array([-1.0, 1.0]),
                    position,
                )
        top_bound = max(position[1], top_bound)
        left_bound = min(position[0], left_bound)
        bottom_bound = min(position[1], bottom_bound)
        if movement == 0:
            break

    # Reset position and attempt to move rightwards
    position = initial_position.copy()
    while True:
        position, movement = directional_walk(
            image,
            background_image,
            is_daytime,
            np.array([1.0, 0.0]),
            position,
        )
        if movement == 0:
            position, movement = directional_walk(
                image,
                background_image,
                is_daytime,
                np.array([1.0, -1.0]),
                position,
            )
            if movement == 0:
                position, movement = directional_walk(
                    image,
                    background_image,
                    is_daytime,
                    np.array([1.0, 1.0]),
                    position,
                )
        top_bound = max(position[1], top_bound)
        right_bound = max(position[0], right_bound)
        bottom_bound = min(position[1], bottom_bound)
        if movement == 0:
            break

    return left_bound, right_bound, top_bound, bottom_bound


def overlap(
    left1: Union[int, float],
    right1: Union[int, float],
    top1: Union[int, float],
    bottom1: Union[int, float],
    left2: Union[int, float],
    right2: Union[int, float],
    top2: Union[int, float],
    bottom2: Union[int, float],
) -> float:
    """
    Calculate the overlap area between two rectangular regions.

    Given the bounding coordinates of two rectangles, this function calculates
    the overlap area by determining the intersecting width and height. If there
    is no overlap, the area is zero.

    Args:
        left1 (Union[int, float]): Left x-coordinate of the first rectangle.
        right1 (Union[int, float]): Right x-coordinate of the first rectangle.
        top1 (Union[int, float]): Top y-coordinate of the first rectangle.
        bottom1 (Union[int, float]): Bottom y-coordinate of the first rectangle.
        left2 (Union[int, float]): Left x-coordinate of the second rectangle.
        right2 (Union[int, float]): Right x-coordinate of the second rectangle.
        top2 (Union[int, float]): Top y-coordinate of the second rectangle.
        bottom2 (Union[int, float]): Bottom y-coordinate of the second rectangle.

    Returns:
        float: The area of overlap between the two rectangles.
    """
    horizontal_overlap = max(min(right1, right2) - max(left1, left2), 0)
    vertical_overlap = max(min(top1, top2) - max(bottom1, bottom2), 0)
    overlap_area = horizontal_overlap * vertical_overlap

    return overlap_area


def directional_walk(
    image: np.ndarray,
    background_image: np.ndarray,
    is_daytime: bool,
    direction: np.ndarray,
    start_position: np.ndarray,
) -> Tuple[np.ndarray, int]:
    """
    Move an object in a specified direction within an image, checking for changes
    compared to the background image, and return the final position and movement status.

    The function moves the object step-by-step, checking if each movement results
    in a change in pixel values compared to the background image. Movement stops
    when no significant change is detected or when the boundaries of the image are reached.

    Args:
        image (np.ndarray): The current image.
        background_image (np.ndarray): The background image for comparison.
        is_daytime (bool): Flag indicating if daytime background tolerance should be used.
        direction (np.ndarray): The direction vector for movement.
        start_position (np.ndarray): The starting position of the object in the image.

    Returns:
        Tuple[np.ndarray, int]: The final position after movement and a movement status flag (1 if moved, 0 if no movement).
    """
    background_tolerance = (
        ENV.background_tol_day if is_daytime else ENV.background_tol_night
    )

    old_x_pos, old_y_pos = start_position[0], start_position[1]
    image_shape = image.shape

    while True:
        move = 0
        valid_move = 0

        # Check if the move is within bounds
        if 0 < start_position[0] + direction[0] * 5 < image_shape[0]:
            if 0 < start_position[1] + direction[1] * 5 < image_shape[1]:
                valid_move = 1

        if valid_move == 1:
            # Get pixel values at the new position
            image_sample = image[
                int(start_position[0] + direction[0]),
                int(start_position[1] + direction[1]),
            ]
            background_image_sample = background_image[
                int(start_position[0] + direction[0]),
                int(start_position[1] + direction[1]),
            ]

            # Check if the image sample is within the expected color range
            color_test = np.sum(image_sample > ENV.colour_lower) + np.sum(
                image_sample < ENV.colour_upper
            )

            if (
                int(np.max(image_sample)) - int(np.min(image_sample))
                < ENV.greyscale_parameter
                and color_test == 6
            ):
                max_diff = 0
                for k in range(3):
                    max_diff = max(
                        abs(int(background_image_sample[k]) - int(image_sample[k])),
                        max_diff,
                    )

                if max_diff > background_tolerance:
                    # Update position if there is significant change
                    for n in range(len(start_position)):
                        start_position[n] += direction[n]
                    move = 1

        # Stop if no valid movement is detected
        if move == 0:
            break

    # Check if movement occurred
    movement_status = 1
    if old_x_pos == start_position[0] and old_y_pos == start_position[1]:
        movement_status = 0

    return start_position, movement_status
