from import_export import resources, fields
from .models import FoodList


class FoodListResource(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='id')

    class Meta:
        model = FoodList
        fields = ['Category', 'LocalName', 'EnglishName', 'ScientificName', 'ENERC_kJ', 'ENERC_kcal', 'WATER_g',
                  'PROTCNT_g', 'FATCE_g', 'CHOCDF_g', 'FIB_g', 'ASH_g', 'Ca_mg', 'Fe_mg', 'Mg_mg', 'P_mg', 'K_mg',
                  'Na_mg', 'Zn_mg', 'Cu_mg', 'Mn_mg', 'VIT_A_RAE_mcg', 'RETOL_mcg', 'CARTB_mcg', 'VITDEQ_mcg',
                  'VITE_mg', 'THIA_mg', 'RIBF_mg', 'NIAEQ_mg', 'VIT_B6_mg', 'FOL_mcg', 'VITB12_mcg', 'VITC_mg',
                  'SearchName']
        exclude = ('REFID', 'Code', 'FrenchNames', 'Source')
