import matplotlib.pyplot as plt
from typing import List, Tuple
from polygon import MiterOffsetStrategy
from offset_service import CADOffsetService

def plot_case(ax, title: str, input_coords: List[Tuple[float, float]], result_polygons: List['Polygon']):
    ax.set_title(title)
    ax.set_aspect('equal', 'box')
    ax.grid(True, linestyle='--', alpha=0.6)
    in_x = [p[0] for p in input_coords] + [input_coords[0][0]]
    in_y = [p[1] for p in input_coords] + [input_coords[0][1]]
    ax.plot(in_x, in_y, 'k--', label='Input', alpha=0.5, linewidth=1.5)

    if not result_polygons:
        ax.text(0.5, 0.5, "DISAPPEARED", transform=ax.transAxes, 
                ha='center', color='red', fontsize=12, fontweight='bold')
    else:
        for i, poly in enumerate(result_polygons):
            coords = [(p.x, p.y) for p in poly.vertices]
            if not coords: continue
            x = [c[0] for c in coords] + [coords[0][0]]
            y = [c[1] for c in coords] + [coords[0][1]]
            ax.fill(x, y, alpha=0.3, label=f'Result #{i+1}' if i == 0 else "")
            ax.plot(x, y, solid_capstyle='round', linewidth=2)
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='best')

def visualize_all_cases():
    strategy = MiterOffsetStrategy()
    service = CADOffsetService(strategy)
    _, axes = plt.subplots(3, 2, figsize=(12, 16))
    axes = axes.flatten()

    # --- Expansion ---
    case1_in = [(3, 12), (12, 12), (12, 3), (9, 3), (9, 9), (6, 9), (6, 3), (3, 3)]
    res1 = service.offset_polygon(case1_in, d=1)
    plot_case(axes[0], "Case 1: U-Shape (Expand d=1)", case1_in, res1)

    # --- Hole ---
    case2_in = [(4, 10), (18, 10), (18, 4), (12, 4), (10, 6), (8, 4), (4, 4)]
    res2 = service.offset_polygon(case2_in, d=1)
    plot_case(axes[1], "Case 2: Hole Creation (Expand d=1)", case2_in, res2)

    # --- Zero Offset ---
    case3_in = [(0, 0), (10, 0), (10, 10), (0, 10)]
    res3 = service.offset_polygon(case3_in, d=0)
    plot_case(axes[2], "Case 3: Zero Offset (d=0)", case3_in, res3)

    # --- Collapse ---
    case4_in = [(0, 0), (2, 0), (2, 2), (0, 2)]
    res4 = service.offset_polygon(case4_in, d=-5)
    plot_case(axes[3], "Case 4: Full Collapse (Shrink d=-5)", case4_in, res4)

    # --- Split ---
    case5_in = [(2, 9), (8, 9), (8, 2), (6, 2), (6, 8), (4, 8), (4, 2), (2, 2)]
    res5 = service.offset_polygon(case5_in, d=-0.6)
    plot_case(axes[4], "Case 5: Split (Shrink d=-0.6)", case5_in, res5)

    # --- CW/CWW ---
    cw_square = [(0, 0), (0, 5), (5, 5), (5, 0)]
    res6 = service.offset_polygon(cw_square, d=1)
    plot_case(axes[5], "Test: Orientation Check (d=1)", cw_square, res6)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    visualize_all_cases()
