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
        df['other sugars'] = (df['Sugars (g/100g)'] - df[['fructose (g/100g)', 'galactose (g/100g)', 'glucose (g/100g)','lactose (g/100g)', 'maltose (g/100g)', 'sucrose (g/100g)']].sum(axis=1)).apply(lambda x : x if x > 0 else 0)


        df['other carbs'] = (df['Carbohydrate (g/100g)'] - df[['Sugars (g/100g)','Starch (g/100g)','Fibres (g/100g)', 'Polyols (g/100g)']].sum(axis=1)).apply(lambda x : x if x > 0 else 0)


        df['other fats'] = (df['Fat (g/100g)'] - df[['FA saturated (g/100g)', 'FA mono (g/100g)', 'FA poly (g/100g)']].sum(axis=1)).apply(lambda x : x if x > 0 else 0)


        df["Protein kcal"] = df['Protein (g/100g)'] * 4
        df["Carbohydrate kcal"] = df["Carbohydrate (g/100g)"] * 4
        df["Fat kcal"] = df['Fat (g/100g)'] * 9
        df["Alcohol kcal"] = df['Alcohol (g/100g)'] * 7

        # columns_to_drop = ['alim_grp_code', 'alim_ssgrp_code', 'alim_ssssgrp_code',
        #            'alim_grp_nom_eng', 'alim_ssgrp_nom_eng', 'alim_ssssgrp_nom_eng',
        #            'alim_nom_sci', 'Energy, Regulation EU No 1169/2011 (kJ/100g)',
        #            'Energy, N x Jones\' factor, with fibres (kJ/100g)',
        #            'Energy, N x Jones\' factor, with fibres (kcal/100g)',
        #            'Protein, crude, N x 6.25 (g/100g)']
        # df = df.drop(columns_to_drop, axis=1)

        return df

    def _get_row(self,selected_row):
        return self.df.iloc[selected_row[0]] if selected_row else self.df.iloc[0]
    
    def get_table(self):

        columns_to_pick = ['alim_nom_eng','Carbohydrate (g/100g)','Fat (g/100g)','Protein (g/100g)']
        cleaned_df = self.df[columns_to_pick]

        return cleaned_df.to_dict("records")

    def get_calorie_info(self,selected_row):

        row = self._get_row(selected_row)
        
        names = ['Protein kcal','Carbohydrate kcal','Fat kcal','Alcohol kcal']
        values = row[names].to_numpy().transpose().flatten()
        title = row['alim_nom_eng']
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
