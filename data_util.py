from numpy import column_stack
import pandas as pd

class NutrientInfoRepo():


    def __init__(self) -> None:
        self.df = self.load_and_pre_process()
        pass

    
    def load_and_pre_process(self) -> pd.DataFrame:
        df = pd.read_excel("assets/Table Ciqual 2020_ENG_2020 07 07.xls",decimal=",",na_values=["-","traces"]).fillna(0)
        df = df.replace({'< ':'',",":'.'},regex=True)
        df = df.apply(pd.to_numeric,errors="ignore")
        df = df.rename(columns={'alim_nom_eng':'Name','Energy, N x Jones\' factor, with fibres (kcal/100g)':'kcal/100g'})
        df['other sugars'] = (df['Sugars (g/100g)'] - df[['fructose (g/100g)', 'galactose (g/100g)', 'glucose (g/100g)','lactose (g/100g)', 'maltose (g/100g)', 'sucrose (g/100g)']].sum(axis=1)).apply(lambda x : x if x > 0 else 0)


        df['other carbs'] = (df['Carbohydrate (g/100g)'] - df[['Sugars (g/100g)','Starch (g/100g)','Fibres (g/100g)']].sum(axis=1)).apply(lambda x : x if x > 0 else 0)


        df['other fats'] = (df['Fat (g/100g)'] - df[['FA saturated (g/100g)', 'FA mono (g/100g)', 'FA poly (g/100g)']].sum(axis=1)).apply(lambda x : x if x > 0 else 0)


        df["Protein kcal"] = df['Protein (g/100g)'] * 4
        df["Carbohydrate kcal"] = df["Carbohydrate (g/100g)"] * 4
        df["Fat kcal"] = df['Fat (g/100g)'] * 9
        df["Alcohol kcal"] = df['Alcohol (g/100g)'] * 7

        return df

    def _get_row(self,selected_row):
        return self.df.iloc[selected_row[0]] if selected_row else self.df.iloc[0]
    
    def get_dropdown_options(self):
        return ['kcal/100g','Protein (g/100g)',
       'Carbohydrate (g/100g)', 'Fat (g/100g)', 'Sugars (g/100g)',
       'fructose (g/100g)', 'galactose (g/100g)', 'glucose (g/100g)',
       'lactose (g/100g)', 'maltose (g/100g)', 'sucrose (g/100g)',
       'Starch (g/100g)', 'Fibres (g/100g)', 'Polyols (g/100g)',
       'Ash (g/100g)', 'Alcohol (g/100g)', 'Organic acids (g/100g)',
       'FA saturated (g/100g)', 'FA mono (g/100g)', 'FA poly (g/100g)',
       'FA 4:0 (g/100g)', 'FA 6:0 (g/100g)', 'FA 8:0 (g/100g)',
       'FA 10:0 (g/100g)', 'FA 12:0 (g/100g)', 'FA 14:0 (g/100g)',
       'FA 16:0 (g/100g)', 'FA 18:0 (g/100g)', 'FA 18:1 n-9 cis (g/100g)',
       'FA 18:2 9c,12c (n-6) (g/100g)', 'FA 18:3 c9,c12,c15 (n-3) (g/100g)',
       'FA 20:4 5c,8c,11c,14c (n-6) (g/100g)',
       'FA 20:5 5c,8c,11c,14c,17c (n-3) EPA (g/100g)',
       'FA 22:6 4c,7c,10c,13c,16c,19c (n-3) DHA (g/100g)',
       'Cholesterol (mg/100g)', 'Salt (g/100g)', 'Calcium (mg/100g)',
       'Chloride (mg/100g)', 'Copper (mg/100g)', 'Iron (mg/100g)',
       'Iodine (µg/100g)', 'Magnesium (mg/100g)', 'Manganese (mg/100g)',
       'Phosphorus (mg/100g)', 'Potassium (mg/100g)', 'Selenium (µg/100g)',
       'Sodium (mg/100g)', 'Zinc (mg/100g)', 'Retinol (µg/100g)',
       'Beta-carotene (µg/100g)', 'Vitamin D (µg/100g)', 'Vitamin E (mg/100g)',
       'Vitamin K1 (µg/100g)', 'Vitamin K2 (µg/100g)', 'Vitamin C (mg/100g)',
       'Vitamin B1 or Thiamin (mg/100g)', 'Vitamin B2 or Riboflavin (mg/100g)',
       'Vitamin B3 or Niacin (mg/100g)',
       'Vitamin B5 or Pantothenic acid (mg/100g)', 'Vitamin B6 (mg/100g)',
       'Vitamin B9 or Folate (µg/100g)', 'Vitamin B12 (µg/100g)']
    def get_table(self):

        columns_to_pick = ['Name','Carbohydrate (g/100g)','Fat (g/100g)','Protein (g/100g)','Cholesterol (mg/100g)', 'Salt (g/100g)', 'Calcium (mg/100g)',
       'Chloride (mg/100g)', 'Copper (mg/100g)', 'Iron (mg/100g)',
       'Iodine (µg/100g)', 'Magnesium (mg/100g)', 'Manganese (mg/100g)',
       'Phosphorus (mg/100g)', 'Potassium (mg/100g)', 'Selenium (µg/100g)',
       'Sodium (mg/100g)', 'Zinc (mg/100g)', 'Retinol (µg/100g)',
       'Beta-carotene (µg/100g)', 'Vitamin D (µg/100g)', 'Vitamin E (mg/100g)',
       'Vitamin K1 (µg/100g)', 'Vitamin K2 (µg/100g)', 'Vitamin C (mg/100g)',
       'Vitamin B1 or Thiamin (mg/100g)', 'Vitamin B2 or Riboflavin (mg/100g)',
       'Vitamin B3 or Niacin (mg/100g)',
       'Vitamin B5 or Pantothenic acid (mg/100g)', 'Vitamin B6 (mg/100g)',
       'Vitamin B9 or Folate (µg/100g)', 'Vitamin B12 (µg/100g)']

        cleaned_df = self.df[columns_to_pick]

        return cleaned_df.to_dict("records"), columns_to_pick

    def get_category_standardized_df(self):
        return self.df.groupby('alim_grp_nom_eng').mean()
    
    def get_rda_chart(self,selected_row):
        row = self._get_row(selected_row)
        print(row.keys())
        rda_values = {
            'Carbohydrate (g/100g)':130,'Fat (g/100g)':20+35/2,'Protein (g/100g)':56, 'Calcium (mg/100g)':1000,
       'Copper (mg/100g)':0.9, 'Iron (mg/100g)':8,'Magnesium (mg/100g)':400, 'Manganese (mg/100g)':2.3,
       'Phosphorus (mg/100g)':700, 'Potassium (mg/100g)':4700, 'Selenium (µg/100g)':55,
       'Sodium (mg/100g)':2300, 'Zinc (mg/100g)':11, 'Vitamin D (µg/100g)':15, 'Vitamin E (mg/100g)':15, 'Vitamin C (mg/100g)':90,
       'Vitamin B1 or Thiamin (mg/100g)':1.2, 'Vitamin B2 or Riboflavin (mg/100g)':1.3,
       'Vitamin B3 or Niacin (mg/100g)':16, 'Vitamin B6 (mg/100g)':1.3, 'Vitamin B12 (µg/100g)':2.4*1000
        }
        rda_df = pd.DataFrame(columns=['value','nutrient'])
        for nutrient in rda_values:
            print(row[nutrient])
            print(rda_df.head())
            row_d = {'nutrient':nutrient,'value':row[nutrient]*100 / rda_values[nutrient]}

            rda_df = pd.concat([rda_df,pd.DataFrame(row_d,index=[0])])
        
        return rda_df


    def get_calorie_info(self,selected_row):

        row = self._get_row(selected_row)
        
        names = ['Protein kcal','Carbohydrate kcal','Fat kcal','Alcohol kcal']
        values = row[names].to_numpy().transpose().flatten()
        title = row['Name']
        return values,names,title


    def get_nutrient_composition(self,selected_row):

        parents_0 = ['fats','fats','fats','fats','fats','fats','carbohydrates','carbohydrates','carbohydrates','carbohydrates','carbohydrates','carbohydrates','carbohydrates','fats','fats','carbohydrates','carbohydrates','carbohydrates','water','protein','ash','alcohol','organic acids','carbohydrates','fats']
        parents_1 = ['polyunsaturated fats','polyunsaturated fats','polyunsaturated fats','polyunsaturated fats','polyunsaturated fats','polyunsaturated fats','sugars','sugars','sugars','sugars','sugars','sugars','sugars','saturated fats','monounsaturated fats','starch','fibres','polyols',None,None,None,None,None,'no data/other','no data/other']
        parents_2 = ["omega 3","omega 3","omega 3","omega 6","omega 6","omega 9",'fructose', 'galactose', 'glucose','lactose', 'maltose', 'sucrose','no data/other',None,None,None,None,None,None,None,None,None,None,None,None]
        parents_3 = ["ala","epa","dha",'linoleic','arachidonic',None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]

        omega9 = ['FA 18:1 n-9 cis (g/100g)']
        omega6 = ['FA 18:2 9c,12c (n-6) (g/100g)','FA 20:4 5c,8c,11c,14c (n-6) (g/100g)']
        omega3 = ['FA 18:3 c9,c12,c15 (n-3) (g/100g)','FA 20:5 5c,8c,11c,14c,17c (n-3) EPA (g/100g)', 'FA 22:6 4c,7c,10c,13c,16c,19c (n-3) DHA (g/100g)']
        sugars = ['fructose (g/100g)', 'galactose (g/100g)', 'glucose (g/100g)','lactose (g/100g)', 'maltose (g/100g)', 'sucrose (g/100g)','other sugars']

        row = self._get_row(selected_row)

        values = row[omega3 + omega6 + omega9 + sugars + ['FA saturated (g/100g)','FA mono (g/100g)','Starch (g/100g)','Fibres (g/100g)','Polyols (g/100g)','Water (g/100g)','Protein (g/100g)','Ash (g/100g)','Alcohol (g/100g)','Organic acids (g/100g)','other carbs','other fats']]
        values = values.to_numpy().transpose().flatten()
        nutrient_df = pd.DataFrame(
        dict(values=values, parents_3=parents_3, parents_2=parents_2, parents_1= parents_1,parents_0=parents_0))
        path = ['parents_0','parents_1', 'parents_2', 'parents_3']
        return nutrient_df,path,values
