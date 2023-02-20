# based on
# https://microsoft.github.io/dowhy/example_notebooks/tutorial-causal
# inference-machinelearning-using-dowhy-econml.html
# https://microsoft.github.io/dowhy/example_notebooks/dowhy_confounder
# _example.html?highlight=slope

# imports
import matplotlib.pyplot as plt
# import two modules from "dowhy" in one line
import dowhy.datasets, dowhy.plotter
import seaborn as sns

# set treatment (viscosity) as causal for the outcome (performance)
effect = True

# build sample data set
data_dict = dowhy.datasets.xy_dataset(
                20,  # number of samples
                effect=effect,
                num_common_causes=1,
                is_linear=False,
                sd_error=0.75
                )

# get DataFrame
df = data_dict['df']
# rename columns to match the envisioned example
df.columns = ["Viscosity", "Performance", "Temperature", "pH"]
# tune values
df["Temperature"] += 20
df["Performance"] += 75
# show info / DataFrame structure
print(df.head())

# specify "outcome", "treatment" and "cause"; these are the terms
# used in causal analysis
outcome = "Performance"
treatment = "Viscosity"
# one cause
common_causes = "Temperature"
# # two causes
# common_causes = ["Temperature", "pH"]

# plot sample data via (dowhy built-in) function
dowhy.plotter.plot_treatment_outcome(
        df[treatment], 
        df[outcome],
        df["pH"]
        )
# show plot
plt.show()

# make custom "plot_treatment_outcome"-like plot
x = "pH"  # use "pH" as variable on the x axis  
for _c in [treatment, outcome]:
    plt.scatter(
        df[x],
        df[_c],
        label=_c
        )
# plot cosmetics
plt.xlabel(x)
plt.ylabel("\n".join([treatment, outcome]))
plt.legend(frameon=False, fontsize=12)
# save custom plot
plt.savefig(
        "modified_plotter_type.png", 
        dpi=300, 
        bbox_inches="tight"
        )
# show
plt.show()

# pairplot to show variable dependecies
sns.pairplot(
        df, 
        height=3.5, 
        corner=True,  # don't add axes to the upper triangle
        diag_kind="hist"
        )

# save pairplot
plt.savefig(
        "df_pairplot.png", 
        dpi=300
        )

# %% step 1: Model the problem as a causal graph
#

# define model, i.e. build causal graph
model= dowhy.CausalModel(
        data=df,
        treatment=treatment,
        outcome=outcome,
        common_causes=common_causes
        )

# show model
model.view_model(layout="dot")

from IPython.display import Image, display

# save model
display(Image(filename="causal_model.png"))


# %% step 2: Identify causal effect using properties of the formal 
# causal graph
#

identified_estimand = model.identify_effect(
        proceed_when_unidentifiable=True
        )
print(identified_estimand)

# %% step 3: Estimate the causal effect
#

estimate = model.estimate_effect(
            identified_estimand,
            method_name="backdoor.linear_regression"
            )

print(estimate)
# ## Realized estimand
# b: Performance~Viscosity+Temperature
# Target units: ate

# ## Estimate
# Mean value: 1.876112877792039
print(f"DoWhy estimate of causal effect is {estimate.value}")
# DoWhy estimate of causal effect is 1.876112877792039

# Plot slope of line between action and outcome = causal effect
dowhy.plotter.plot_causal_effect(
    estimate, 
    df[treatment], 
    df[outcome]
    )
# show
plt.show()


# %% step 3b: Getting more from the "estimate"
#

# get intercept and slope
intercept = estimate.intercept
slope = estimate.value
# get error information
std_error = estimate.get_standard_error()[0]
ci = estimate.get_confidence_intervals()[0]

# plot "experimental" data and best causal fit
plt.plot(
        df[treatment], 
        df[outcome], 
        "ko",  # black (k) dot markers (o) 
        zorder=1  # plot markers on top layer
        )
plt.plot(
        df[treatment], 
        df[treatment]*slope+intercept, 
        "r-",  # red solid line
         alpha=0.5,  # opacity 
         zorder=1  # plot markers on top layer
         )
# plot fit lines from each experimental point
for _i, _row in df[["Viscosity", "Performance"]].iterrows():
    # info
    for _s in ci:
        plt.axline(
            (_row["Viscosity"], _row["Performance"]), 
            slope=_s,
            alpha=.10,
            zorder=0
            )

# get axes
ax = plt.gca()

# info text
plt.text(0.05, 0.1,  # x and y-coordinates
         f"Slope: {slope:.2f} $\pm$ {std_error:.2f}",  # 2-decimals
         transform=ax.transAxes  # use axes coordinate system
         )

# specify y-range
plt.ylim(bottom=0)
# label cosmetics
plt.xlabel(treatment)
plt.ylabel(outcome)

# get literal results description
estimate.interpret()

# save plot
plt.savefig(
    "modifed_causal_effect.png", 
    dpi=300, 
    bbox_inches="tight"
    )

# show plot
plt.show()

# %% step 4: Refuting the estimate
#

# A) Adding a random common cause variable
res_random = model.refute_estimate(
                identified_estimand, 
                estimate, 
                method_name="random_common_cause"
                )
print(res_random)
# Refute: Add a random common cause
# Estimated effect:1.876112877792039
# New effect:1.876864110685575
# p value:0.49

# B) Replacing treatment with a random (placebo) variable
res_placebo = model.refute_estimate(
                identified_estimand, 
                estimate,
                method_name="placebo_treatment_refuter", 
                placebo_type="permute"
                )
print(res_placebo)
# Refute: Use a Placebo Treatment
# Estimated effect:1.876112877792039
# New effect:0.025135938683012428
# p value:0.48
