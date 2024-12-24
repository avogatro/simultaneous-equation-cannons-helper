"""
Class to find Color for heatmap
"""

from materialyoucolor.palettes.tonal_palette import TonalPalette

class HctColorFinder:
    """
    Class to find Color for heatmap
    """
    hue : int
    chroma: int
    tone: int = 50

    def __init__(self, chroma, tone = 50):

        self.chroma = chroma
        self.tone = tone

    def find_colors(self, total_steps : int):
        """
        find colors with different hue, same chroma, tone
        """
        res= []
        hue_step = 360.0/total_steps
        for i in range(total_steps):
            color = TonalPalette.from_hue_and_chroma(i * hue_step+180, self.chroma)
            color_rgba = color.get_hct(self.tone+(i%2)*20).to_rgba()
            color_hex = f"#{color_rgba[0]:02x}{color_rgba[1]:02x}{color_rgba[2]:02x}{color_rgba[3]:02x}"
            res.append(color_hex)
        return res
