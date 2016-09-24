import iofunctions as iof
import os
import pandas as pd

datafolder = "data"

# laod all Imaris CSV files
spinefiles = iof.list_files(datafolder,"csv")

for spinefile in spinefiles:
    location = os.path.join(datafolder, spinefile)



MergedSpineData = pd.DataFrame()
for spinefile in spinefiles:
    location = os.path.join(datafolder, spinefile)
    try:
        SingleSpineData = pd.read_csv(location, index_col=13)
        totalSpineMeasures = len(SingleSpineData[SingleSpineData.Variable == "Spine Length"])
        totalDendriteLength = SingleSpineData.loc[SingleSpineData["Variable"] == "Dendrite Length", "Value"].sum()
        
        # adding a column with 2D Spine Density
        SingleSpineData["2D Spine Density"] = 0.5*totalSpineMeasures/totalDendriteLength
        SingleSpineData["ImageName"] = spinefile
        # check that there are no problems with odd/even spine number
        if (totalSpineMeasures % 2 == 0):
            # merge all spinefiles in one
            MergedSpineData = pd.concat([MergedSpineData, SingleSpineData])
        else:
            print("ERROR Odd: "+spinefile)
    except:
        print("ERROR Format CSV, removing it: "+spinefile)
        f = open(spinefile,"r+")
        d = f.readlines()
        f.seek(0)
        #remove Imaris-exported shit of the first 3 lines
        del d[0:2]
        for i in d:
            if i != "line you want to remove...":
                f.write(i)
        f.truncate()
        f.close()

SpineLengthMixed = MergedSpineData[MergedSpineData.Variable == "Spine Length"].reset_index()
SpineStraightMixed = MergedSpineData[MergedSpineData.Variable == "Spine Straightness"].reset_index()
# extracting data from SpineLengthMixed
SpineLength = SpineLengthMixed[SpineLengthMixed.index % 2 == 0].reset_index()
SpineWidth = SpineLengthMixed[SpineLengthMixed.index % 2 == 1].reset_index()
SpineStraightness = SpineStraightMixed[SpineStraightMixed.index % 2 == 0].reset_index()

totalSpines = len(SpineLength)
print("\n================\nTotal Spines: "+str(totalSpines))

SpineStraightness.head()

mergedSpineDF = pd.DataFrame()
mergedSpineDF = pd.concat([SpineLength.Value, SpineWidth.Value, SpineLength["2D Spine Density"], SpineStraightness.Value, SpineLength.ImageName], axis=1)
mergedSpineDF.columns = ["Spine Length, um", "Head Width, um", "2D Spine Density 1/um", "Straightness", "Image Name"]

mergedSpineDF.tail()