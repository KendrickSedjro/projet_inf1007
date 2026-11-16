"""Test du graphique d'exploration."""
import pandas as pd

from exploration import tracer_distributions


def test_tracer_distributions_cree_l_image(tmp_path):
    df = pd.DataFrame({s: [50, 60, 70] for s in ["PAC", "SHO", "PAS", "DRI", "DEF", "PHY"]})
    chemin = str(tmp_path / "graphique.png")
    assert tracer_distributions(df, chemin) == chemin
    assert (tmp_path / "graphique.png").exists()