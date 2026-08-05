class CoordinateTranslator:
    """Utility class handling coordinate conversions between native image resolution

    and display canvas viewports across arbitrary zoom levels.
    """

    def __init__(self, native_res=(908, 871), base_display_res=(680, 600)):
        self.orig_w, self.orig_h = native_res
        self.base_w, self.base_h = base_display_res

    def set_base_height(self, height):
        """Dynamically set the base display height for responsive scaling.

        This allows the translator to adapt to actual container dimensions
        rather than using hardcoded values. Call this with the available
        container height before rendering.

        Args:
            height: The actual available display height in pixels
        """
        if height > 0:
            self.base_h = int(height)
            # Maintain aspect ratio for width
            aspect_ratio = self.orig_w / self.orig_h if self.orig_h > 0 else 1.0
            self.base_w = int(self.base_h * aspect_ratio)

    def get_display_dimensions(self, zoom_level=1.0):
        """Calculates current pixel width and height based on zoom level, preserving aspect ratio."""
        # Calculate display dimensions while maintaining aspect ratio
        aspect_ratio = self.orig_w / self.orig_h if self.orig_h > 0 else 1.0

        # Start with base height and calculate width to maintain aspect ratio
        disp_h = int(self.base_h * zoom_level)
        disp_w = int(disp_h * aspect_ratio)

        return disp_w, disp_h

    def get_scale_factors(self, zoom_level=1.0):
        """Calculates width/height scale ratios from native resolution to zoomed display."""
        disp_w, disp_h = self.get_display_dimensions(zoom_level)
        scale_x = disp_w / float(self.orig_w)
        scale_y = disp_h / float(self.orig_h)
        return scale_x, scale_y

    def native_to_canvas(self, native_coords, zoom_level=1.0, offset=(10, 10)):
        """Converts [x1, y1, x2, y2] from native image space to Canvas pixel coordinates."""
        scale_x, scale_y = self.get_scale_factors(zoom_level)
        x_off, y_off = offset

        x1 = x_off + (native_coords[0] * scale_x)
        y1 = y_off + (native_coords[1] * scale_y)
        x2 = x_off + (native_coords[2] * scale_x)
        y2 = y_off + (native_coords[3] * scale_y)

        return x1, y1, x2, y2

    def canvas_to_native(self, canvas_coords, zoom_level=1.0, offset=(10, 10)):
        """Converts [x1, y1, x2, y2] from Canvas pixel coordinates back to native image resolution."""
        scale_x, scale_y = self.get_scale_factors(zoom_level)
        x_off, y_off = offset

        native_x1 = int((canvas_coords[0] - x_off) / scale_x)
        native_y1 = int((canvas_coords[1] - y_off) / scale_y)
        native_x2 = int((canvas_coords[2] - x_off) / scale_x)
        native_y2 = int((canvas_coords[3] - y_off) / scale_y)

        return [native_x1, native_y1, native_x2, native_y2]