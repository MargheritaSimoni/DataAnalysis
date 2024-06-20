import glob
import argparse
import ROOT

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Plot histograms from ROOT files")
    parser.add_argument("files_pattern", help="Wildcard pattern to match ROOT files")
    parser.add_argument("hist_name", help="Name of the histogram to plot")
    parser.add_argument("--xlog", action="store_true", help="Plot with x-axis in log scale")
    parser.add_argument("--loglog", action="store_true", help="Plot with both axes in log scale")
    args = parser.parse_args()

    # Use glob to find files matching the pattern
    files = glob.glob(args.files_pattern)
    if not files:
        print(f"No files found matching pattern: {args.files_pattern}")
        return

    # Initialize a ROOT canvas
    canvas = ROOT.TCanvas("canvas", "Canvas", 800, 600)

    # Set log scale if requested
    if args.xlog or args.loglog:
        canvas.SetLogx()
    if args.loglog:
        canvas.SetLogy()

    # Variable to hold the first histogram for plotting
    first_hist = None
    color_index = 1

    # List to hold open ROOT files
    open_files = []

    # Create a legend in the bottom right corner
    legend = ROOT.TLegend(0.7, 0.1, 0.9, 0.3)

    # Loop over files and retrieve histograms
    for file_name in files:
        root_file = ROOT.TFile.Open(file_name)
        if not root_file or root_file.IsZombie():
            print(f"Failed to open file: {file_name}")
            continue

        hist = root_file.Get(args.hist_name)
        if not hist:
            print(f"Histogram {args.hist_name} not found in file: {file_name}")
            root_file.Close()
            continue

        hist.SetLineColor(color_index)
        hist.SetLineWidth(2)

        # Draw the first histogram
        if first_hist is None:
            first_hist = hist
            first_hist.Draw()
        else:
            hist.Draw("SAME")

        # Add histogram to the legend
        legend.AddEntry(hist, file_name, "l")

        color_index += 1
        open_files.append(root_file)

    # Draw the legend
    legend.Draw()

    # Save the plot to the output file
    canvas.SaveAs("IstogramsPlotOutput.png")

    # Close all open ROOT files
    for root_file in open_files:
        root_file.Close()

if __name__ == "__main__":
    main()
