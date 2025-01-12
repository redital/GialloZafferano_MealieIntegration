from dataclasses import dataclass, asdict
from typing import Optional
import uuid
import json


@dataclass
class IngredientUnit:
    name: str
    id: Optional[str] = str(uuid.uuid4())
    description: str = ""
    extras: dict = ""
    fraction: bool = False
    abbreviation: str = None
    useAbbreviation: bool = False
    
    def serialize(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)   

@dataclass
class IngredientFood:
    name: str
    id: Optional[str] = str(uuid.uuid4())
    description: str = ""
    puralName: str = ""
    extras: dict = ""
    onHand: bool = False
    aliases: list[dict] = None
    
    def serialize(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

@dataclass
class RecipeIngredient:
    food: IngredientFood
    quantity: float
    isFood: bool
    disableAmount: bool
    display: str
    unit: Optional[IngredientUnit] = None
    note: Optional[str] = None
    title: Optional[str] = None
    originalText: Optional[str] = None
    referenceId: Optional[str] = str(uuid.uuid4())
    
    def serialize(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

@dataclass
class RecipeInstruction:
    title: str
    text: str
    ingredientReferences: list[str]
    id: Optional[str] = str(uuid.uuid4())
    
    def serialize(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

@dataclass
class Nutrition:
    calories: Optional[float] = None
    fatContent: Optional[float] = None
    proteinContent: Optional[float] = None
    carbohydrateContent: Optional[float] = None
    fiberContent: Optional[float] = None
    sodiumContent: Optional[float] = None
    sugarContent: Optional[float] = None
    
    def serialize(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

@dataclass
class Settings:
    public: bool
    showNutrition: bool
    showAssets: bool
    landscapeView: bool
    disableComments: bool
    disableAmount: bool
    locked: bool
    
    def serialize(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

@dataclass
class RecipeTag:
    name: str
    slug: str
    id: str = None
    
    def serialize(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

@dataclass
class RecipeCategory:
    name: str
    slug: str
    id: str = None

    def serialize(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

@dataclass
class RecipeTool:
    name: str
    slug: str
    id: str = None
    onHand: bool = False
    
    def serialize(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

@dataclass
class Recipe:
    name: str
    slug: str
    recipeYield: str
    totalTime: str
    description: str
    recipeCategory: list[RecipeCategory]
    tags: list[RecipeTag]
    tools: list[RecipeTool]
    orgURL: str
    dateAdded: str
    dateUpdated: str
    createdAt: str
    updateAt: str
    recipeIngredient: list[RecipeIngredient]
    recipeInstructions: list[RecipeInstruction]
    nutrition: Nutrition
    settings: Settings
    assets: list[dict]
    notes: list[dict]
    extras: dict
    comments: list[dict]
    id: Optional[str] = str(uuid.uuid4())
    userId: Optional[str] = str(uuid.uuid4())
    groupId: Optional[str] = str(uuid.uuid4())
    image: Optional[str] = None
    prepTime: Optional[str] = None
    cookTime: Optional[str] = None
    performTime: Optional[str] = None
    rating: Optional[float] = None
    lastMade: Optional[str] = None

    def serialize(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)
