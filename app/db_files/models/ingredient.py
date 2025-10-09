from pydantic import BaseModel, Field
from typing import Optional


class Nutrients(BaseModel):
        # --- Energy (kJ + kcal) ---
    energy_kj_100g: Optional[float] = None
    energy_kcal_100g: Optional[float] = None
    energy_kj_serving: Optional[float] = None
    energy_kcal_serving: Optional[float] = None

    # --- Macros ---
    carbohydrates_100g: Optional[float] = None
    carbohydrates_serving: Optional[float] = None
    sugars_100g: Optional[float] = None
    sugars_serving: Optional[float] = None
    starch_100g: Optional[float] = None
    starch_serving: Optional[float] = None
    maltodextrins_100g: Optional[float] = None
    maltodextrins_serving: Optional[float] = None
    polyols_100g: Optional[float] = None
    polyols_serving: Optional[float] = None

    proteins_100g: Optional[float] = None
    proteins_serving: Optional[float] = None

    fat_100g: Optional[float] = None
    fat_serving: Optional[float] = None
    saturated_fat_100g: Optional[float] = Field(None, alias="saturated-fat_100g")
    saturated_fat_serving: Optional[float] = Field(None, alias="saturated-fat_serving")
    monounsaturated_fat_100g: Optional[float] = Field(None, alias="monounsaturated-fat_100g")
    monounsaturated_fat_serving: Optional[float] = Field(None, alias="monounsaturated-fat_serving")
    polyunsaturated_fat_100g: Optional[float] = Field(None, alias="polyunsaturated-fat_100g")
    polyunsaturated_fat_serving: Optional[float] = Field(None, alias="polyunsaturated-fat_serving")
    trans_fat_100g: Optional[float] = Field(None, alias="trans-fat_100g")
    trans_fat_serving: Optional[float] = Field(None, alias="trans-fat_serving")
    cholesterol_100g: Optional[float] = None
    cholesterol_serving: Optional[float] = None

    fiber_100g: Optional[float] = None
    fiber_serving: Optional[float] = None
    alcohol_100g: Optional[float] = None
    alcohol_serving: Optional[float] = None

    # --- Specific sugars ---
    sucrose_100g: Optional[float] = None
    sucrose_serving: Optional[float] = None
    glucose_100g: Optional[float] = None
    glucose_serving: Optional[float] = None
    fructose_100g: Optional[float] = None
    fructose_serving: Optional[float] = None
    lactose_100g: Optional[float] = None
    lactose_serving: Optional[float] = None
    maltose_100g: Optional[float] = None
    maltose_serving: Optional[float] = None

    # --- Fatty acids (families) ---
    omega_3_fat_100g: Optional[float] = Field(None, alias="omega-3-fat_100g")
    omega_3_fat_serving: Optional[float] = Field(None, alias="omega-3-fat_serving")
    omega_6_fat_100g: Optional[float] = Field(None, alias="omega-6-fat_100g")
    omega_6_fat_serving: Optional[float] = Field(None, alias="omega-6-fat_serving")
    omega_9_fat_100g: Optional[float] = Field(None, alias="omega-9-fat_100g")
    omega_9_fat_serving: Optional[float] = Field(None, alias="omega-9-fat_serving")

    # --- Fatty acids (examples/subtypes) ---
    alpha_linolenic_acid_100g: Optional[float] = Field(None, alias="alpha-linolenic-acid_100g")
    alpha_linolenic_acid_serving: Optional[float] = Field(None, alias="alpha-linolenic-acid_serving")
    eicosapentaenoic_acid_100g: Optional[float] = Field(None, alias="eicosapentaenoic-acid_100g")
    eicosapentaenoic_acid_serving: Optional[float] = Field(None, alias="eicosapentaenoic-acid_serving")
    docosahexaenoic_acid_100g: Optional[float] = Field(None, alias="docosahexaenoic-acid_100g")
    docosahexaenoic_acid_serving: Optional[float] = Field(None, alias="docosahexaenoic-acid_serving")

    linoleic_acid_100g: Optional[float] = Field(None, alias="linoleic-acid_100g")
    linoleic_acid_serving: Optional[float] = Field(None, alias="linoleic-acid_serving")
    arachidonic_acid_100g: Optional[float] = Field(None, alias="arachidonic-acid_100g")
    arachidonic_acid_serving: Optional[float] = Field(None, alias="arachidonic-acid_serving")
    gamma_linolenic_acid_100g: Optional[float] = Field(None, alias="gamma-linolenic-acid_100g")
    gamma_linolenic_acid_serving: Optional[float] = Field(None, alias="gamma-linolenic-acid_serving")
    dihomo_gamma_linolenic_acid_100g: Optional[float] = Field(None, alias="dihomo-gamma-linolenic-acid_100g")
    dihomo_gamma_linolenic_acid_serving: Optional[float] = Field(None, alias="dihomo-gamma-linolenic-acid_serving")
    oleic_acid_100g: Optional[float] = Field(None, alias="oleic-acid_100g")
    oleic_acid_serving: Optional[float] = Field(None, alias="oleic-acid_serving")
    elaidic_acid_100g: Optional[float] = Field(None, alias="elaidic-acid_100g")
    elaidic_acid_serving: Optional[float] = Field(None, alias="elaidic-acid_serving")
    gondoic_acid_100g: Optional[float] = Field(None, alias="gondoic-acid_100g")
    gondoic_acid_serving: Optional[float] = Field(None, alias="gondoic-acid_serving")
    mead_acid_100g: Optional[float] = Field(None, alias="mead-acid_100g")
    mead_acid_serving: Optional[float] = Field(None, alias="mead-acid_serving")
    erucic_acid_100g: Optional[float] = Field(None, alias="erucic-acid_100g")
    erucic_acid_serving: Optional[float] = Field(None, alias="erucic-acid_serving")
    nervonic_acid_100g: Optional[float] = Field(None, alias="nervonic-acid_100g")
    nervonic_acid_serving: Optional[float] = Field(None, alias="nervonic-acid_serving")

    # --- Saturated chain acids (examples) ---
    butyric_acid_100g: Optional[float] = Field(None, alias="butyric-acid_100g")
    butyric_acid_serving: Optional[float] = Field(None, alias="butyric-acid_serving")
    caproic_acid_100g: Optional[float] = Field(None, alias="caproic-acid_100g")
    caproic_acid_serving: Optional[float] = Field(None, alias="caproic-acid_serving")
    caprylic_acid_100g: Optional[float] = Field(None, alias="caprylic-acid_100g")
    caprylic_acid_serving: Optional[float] = Field(None, alias="caprylic-acid_serving")
    capric_acid_100g: Optional[float] = Field(None, alias="capric-acid_100g")
    capric_acid_serving: Optional[float] = Field(None, alias="capric-acid_serving")
    lauric_acid_100g: Optional[float] = Field(None, alias="lauric-acid_100g")
    lauric_acid_serving: Optional[float] = Field(None, alias="lauric-acid_serving")
    myristic_acid_100g: Optional[float] = Field(None, alias="myristic-acid_100g")
    myristic_acid_serving: Optional[float] = Field(None, alias="myristic-acid_serving")
    palmitic_acid_100g: Optional[float] = Field(None, alias="palmitic-acid_100g")
    palmitic_acid_serving: Optional[float] = Field(None, alias="palmitic-acid_serving")
    stearic_acid_100g: Optional[float] = Field(None, alias="stearic-acid_100g")
    stearic_acid_serving: Optional[float] = Field(None, alias="stearic-acid_serving")
    arachidic_acid_100g: Optional[float] = Field(None, alias="arachidic-acid_100g")
    arachidic_acid_serving: Optional[float] = Field(None, alias="arachidic-acid_serving")
    behenic_acid_100g: Optional[float] = Field(None, alias="behenic-acid_100g")
    behenic_acid_serving: Optional[float] = Field(None, alias="behenic-acid_serving")
    lignoceric_acid_100g: Optional[float] = Field(None, alias="lignoceric-acid_100g")
    lignoceric_acid_serving: Optional[float] = Field(None, alias="lignoceric-acid_serving")
    cerotic_acid_100g: Optional[float] = Field(None, alias="cerotic-acid_100g")
    cerotic_acid_serving: Optional[float] = Field(None, alias="cerotic-acid_serving")
    montanic_acid_100g: Optional[float] = Field(None, alias="montanic-acid_100g")
    montanic_acid_serving: Optional[float] = Field(None, alias="montanic-acid_serving")
    melissic_acid_100g: Optional[float] = Field(None, alias="melissic-acid_100g")
    melissic_acid_serving: Optional[float] = Field(None, alias="melissic-acid_serving")

    # --- Vitamins ---
    vitamin_a_100g: Optional[float] = Field(None, alias="vitamin-a_100g")
    vitamin_a_serving: Optional[float] = Field(None, alias="vitamin-a_serving")
    vitamin_d_100g: Optional[float] = Field(None, alias="vitamin-d_100g")
    vitamin_d_serving: Optional[float] = Field(None, alias="vitamin-d_serving")
    vitamin_e_100g: Optional[float] = Field(None, alias="vitamin-e_100g")
    vitamin_e_serving: Optional[float] = Field(None, alias="vitamin-e_serving")
    vitamin_k_100g: Optional[float] = Field(None, alias="vitamin-k_100g")
    vitamin_k_serving: Optional[float] = Field(None, alias="vitamin-k_serving")
    vitamin_c_100g: Optional[float] = Field(None, alias="vitamin-c_100g")
    vitamin_c_serving: Optional[float] = Field(None, alias="vitamin-c_serving")
    vitamin_b1_100g: Optional[float] = Field(None, alias="vitamin-b1_100g")
    vitamin_b1_serving: Optional[float] = Field(None, alias="vitamin-b1_serving")
    vitamin_b2_100g: Optional[float] = Field(None, alias="vitamin-b2_100g")
    vitamin_b2_serving: Optional[float] = Field(None, alias="vitamin-b2_serving")
    vitamin_pp_100g: Optional[float] = Field(None, alias="vitamin-pp_100g")  # niacin
    vitamin_pp_serving: Optional[float] = Field(None, alias="vitamin-pp_serving")
    vitamin_b6_100g: Optional[float] = Field(None, alias="vitamin-b6_100g")
    vitamin_b6_serving: Optional[float] = Field(None, alias="vitamin-b6_serving")
    vitamin_b9_100g: Optional[float] = Field(None, alias="vitamin-b9_100g")
    vitamin_b9_serving: Optional[float] = Field(None, alias="vitamin-b9_serving")
    vitamin_b12_100g: Optional[float] = Field(None, alias="vitamin-b12_100g")
    vitamin_b12_serving: Optional[float] = Field(None, alias="vitamin-b12_serving")
    biotin_100g: Optional[float] = None
    biotin_serving: Optional[float] = None
    pantothenic_acid_100g: Optional[float] = Field(None, alias="pantothenic-acid_100g")
    pantothenic_acid_serving: Optional[float] = Field(None, alias="pantothenic-acid_serving")

    # --- Minerals / electrolytes ---
    silica_100g: Optional[float] = None
    silica_serving: Optional[float] = None
    bicarbonate_100g: Optional[float] = None
    bicarbonate_serving: Optional[float] = None
    potassium_100g: Optional[float] = None
    potassium_serving: Optional[float] = None
    chloride_100g: Optional[float] = None
    chloride_serving: Optional[float] = None
    calcium_100g: Optional[float] = None
    calcium_serving: Optional[float] = None
    phosphorus_100g: Optional[float] = None
    phosphorus_serving: Optional[float] = None
    iron_100g: Optional[float] = None
    iron_serving: Optional[float] = None
    magnesium_100g: Optional[float] = None
    magnesium_serving: Optional[float] = None
    zinc_100g: Optional[float] = None
    zinc_serving: Optional[float] = None
    copper_100g: Optional[float] = None
    copper_serving: Optional[float] = None
    manganese_100g: Optional[float] = None
    manganese_serving: Optional[float] = None
    fluoride_100g: Optional[float] = None
    fluoride_serving: Optional[float] = None
    selenium_100g: Optional[float] = None
    selenium_serving: Optional[float] = None
    chromium_100g: Optional[float] = None
    chromium_serving: Optional[float] = None
    molybdenum_100g: Optional[float] = None
    molybdenum_serving: Optional[float] = None
    iodine_100g: Optional[float] = None
    iodine_serving: Optional[float] = None

    # --- Other compounds ---
    caffeine_100g: Optional[float] = None
    caffeine_serving: Optional[float] = None
    taurine_100g: Optional[float] = None
    taurine_serving: Optional[float] = None
    casein_100g: Optional[float] = None
    casein_serving: Optional[float] = None
    serum_proteins_100g: Optional[float] = Field(None, alias="serum-proteins_100g")
    serum_proteins_serving: Optional[float] = Field(None, alias="serum-proteins_serving")
    nucleotides_100g: Optional[float] = None
    nucleotides_serving: Optional[float] = None

    # --- Special OFF numerics sometimes under nutriments ---
    sodium_100g: Optional[float] = None
    sodium_serving: Optional[float] = None
    salt_100g: Optional[float] = None
    salt_serving: Optional[float] = None
    ph_100g: Optional[float] = Field(None, alias="ph_100g")
    ph_serving: Optional[float] = Field(None, alias="ph_serving")
    carbon_footprint_100g: Optional[float] = Field(None, alias="carbon-footprint_100g")
    carbon_footprint_serving: Optional[float] = Field(None, alias="carbon-footprint_serving")
    fruits_vegetables_nuts_estimate_100g: Optional[float] = Field(None, alias="fruits-vegetables-nuts-estimate_100g")
    nutrition_score_fr_100g: Optional[float] = Field(None, alias="nutrition-score-fr_100g")
    nutrition_score_uk_100g: Optional[float] = Field(None, alias="nutrition-score-uk_100g")
    cocoa_100g: Optional[float] = None
    cocoa_serving: Optional[float] = None


class IngredientDoc(BaseModel):
    barcode: str = Field(..., alias="code", min_length=4)
    name: Optional[str] = Field(default=None, alias="product_name")
    nutrients: Nutrients

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
        extra = "ignore"

    def to_mongo(self) -> dict:
        """Return a Mongo-ready dict with `_id` = barcode and no Nones."""
        def prune(o):
            if isinstance(o, dict):
                return {k: prune(v) for k, v in o.items() if v is not None and v != []}
            return o
        d = prune(self.model_dump(by_alias=False))
        d["_id"] = d.pop("barcode")
        return d

# --- OFF → minimal IngredientDoc mapper ---
def off_to_minimal(product: dict) -> IngredientDoc:
    n = product.get("nutriments") or {}
    # OFF sometimes uses both energy-kcal_100g and energy_kcal_100g keys
    kcal_100g = n.get("energy-kcal_100g", n.get("energy_kcal_100g"))
    return IngredientDoc(
        code=product.get("code"),                    # alias -> barcode
        product_name=product.get("product_name"),    # alias -> name
        nutrients=Nutrients(
            energy_kcal_100g=kcal_100g,
            protein_100g=n.get("proteins_100g"),
            carbs_100g=n.get("carbohydrates_100g"),
            sugars_100g=n.get("sugars_100g"),
            fat_100g=n.get("fat_100g"),
            sat_fat_100g=n.get("saturated-fat_100g"),
            fiber_100g=n.get("fiber_100g"),
            salt_100g=n.get("salt_100g"),
            sodium_100g=n.get("sodium_100g"),
        ),
    )