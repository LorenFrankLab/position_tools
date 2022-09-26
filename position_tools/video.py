try:
    import cv2
    import numpy as np
    from tqdm.auto import tqdm


    def flip_y(data, frame_size):
        """Flips the y-axis

        Parameters
        ----------
        data : ndarray, shape (n_time, 2)
        frame_size : array_like, shape (2,)

        Returns
        -------
        flipped_data : ndarray, shape (n_time, 2)

        """
        new_data = data.copy()
        if data.ndim > 1:
            new_data[:, 1] = frame_size[1] - new_data[:, 1]
        else:
            new_data[1] = frame_size[1] - new_data[1]
        return new_data


    def convert_to_cm(data, frame_size, cm_to_pixels=1.0):
        """Converts from pixels to cm and flips the y-axis.

        Parameters
        ----------
        data : ndarray, shape (n_time, 2)
        frame_size : array_like, shape (2,)
        cm_to_pixels : float

        Returns
        -------
        converted_data : ndarray, shape (n_time, 2)

        """
        return flip_y(data, frame_size) * cm_to_pixels


    def convert_to_pixels(data, frame_size, cm_to_pixels=1.0):
        """Converts from cm to pixels and flips the y-axis.

        Parameters
        ----------
        data : ndarray, shape (n_time, 2)
        frame_size : array_like, shape (2,)
        cm_to_pixels : float

        Returns
        -------
        converted_data : ndarray, shape (n_time, 2)

        """
        return flip_y(data / cm_to_pixels, frame_size)


    def make_video(video_filename, back_LED, front_LED, head_position,
                head_orientation, output_video_filename='output.avi',
                cm_to_pixels=1.0, disable_progressbar=False):
        RGB_PINK = (234, 82, 111)
        RGB_YELLOW = (253, 231, 76)
        RGB_WHITE = (255, 255, 255)

        RADIUS = 3  # cm

        video = cv2.VideoCapture(video_filename)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        frame_size = int(video.get(3)), int(video.get(4))
        frame_rate = video.get(5)
        n_frames = int(back_LED.shape[0])

        out = cv2.VideoWriter(output_video_filename, fourcc, frame_rate,
                            frame_size, True)

        # Convert to pixels
        back_LED = convert_to_pixels(np.asarray(
            back_LED), frame_size, cm_to_pixels)
        front_LED = convert_to_pixels(np.asarray(
            front_LED), frame_size, cm_to_pixels)

        head_orientation = np.asarray(head_orientation)
        head_orient_end = (np.asarray(head_position) +
                        RADIUS * np.stack((np.cos(head_orientation),
                                            np.sin(head_orientation)), axis=1))

        head_position = convert_to_pixels(np.asarray(
            head_position), frame_size, cm_to_pixels)

        head_orient_start = head_position.copy()
        head_orient_end = convert_to_pixels(
            head_orient_end, frame_size, cm_to_pixels)

        for time_ind in tqdm(range(n_frames - 1), desc='frames',
                            disable=disable_progressbar):
            is_grabbed, frame = video.read()
            if is_grabbed:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                if ~np.any(np.isnan(back_LED[time_ind])):
                    cv2.circle(frame,
                            tuple(back_LED[time_ind].astype(int)),
                            8,
                            RGB_YELLOW,
                            -1,
                            cv2.CV_8U)

                if ~np.any(np.isnan(front_LED[time_ind])):
                    cv2.circle(frame,
                            tuple(front_LED[time_ind].astype(int)),
                            8,
                            RGB_PINK,
                            -1,
                            cv2.CV_8U)

                if (~np.any(np.isnan(head_orient_start[time_ind])) &
                        ~np.any(np.isnan(head_orient_end[time_ind]))):
                    cv2.arrowedLine(frame,
                                    tuple(head_orient_start[time_ind].astype(int)),
                                    tuple(head_orient_end[time_ind].astype(int)),
                                    RGB_WHITE,
                                    4,
                                    8,
                                    0,
                                    0.25)
                if ~np.any(np.isnan(head_position[time_ind])):
                    cv2.circle(frame,
                            tuple(head_position[time_ind].astype(int)),
                            8,
                            RGB_WHITE,
                            -1,
                            cv2.CV_8U)

                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                out.write(frame)
            else:
                break

        video.release()
        out.release()
        cv2.destroyAllWindows()
except ImportError:
    pass