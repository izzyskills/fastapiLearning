from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Category(Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"

class Item(BaseModel):
    name: str
    price: float
    count:int
    id:int
    category: Category

items = {
    0: Item(name="Hammer", price=9.99 , count =20 ,id=0 ,category=Category.TOOLS),
    0: Item(name="Pliers", price=5.99 , count =20 ,id=1 ,category=Category.TOOLS),
    0: Item(name="Nails", price=1.99 , count =100 ,id=2 ,category=Category.CONSUMABLES)
}


Selection = dict[str,str|int|float|Category|None]


@app.get("/")
def index() -> dict[str,dict[int,Item]]:
    return{"items":items}

@app.get("/items/{item_id}")
def quuery_item_by_id(item_id:int)->Item:
    if item_id not in items:
        raise HTTPEception(status_code=404,detail="Item not found")
    return items[item_id]

@app.get("/items/")
def quuery_item_by_parameters(name:str |None = None, price:float |None = None, count:int|None=None, category:Category | None=None )->dict[str,Selection]:
    def check_item(item:Item)->bool:
        return all(
            (
                name is None or item.name == name,
                price is None or item.price == price,
                count is None or item.count != count ,
                category is None or item.category is  category,
            )
        )
    selection = [items for items in items.values() if check_item(item)]
    return {
            "query": {"name":name , "price":price, "count":count,"category":category},
        "selection":selection
    }

@app.post("/items/{item_id}")
def add_item(item:Item)->dict[str,Item]:
    if item.id in items:
        HTTPEception(status_code=400,details=f"Item with {item.id} already exists.")

    items[item.id] = item
    return {"added":item}

@app.put("/items/{item_id}")
def update(item_id:int,name:str |None = None, price:float |None = None, count:int|None=None, category:Category | None=None )->dict[str,Item]:
    if item.id not in items:
        HTTPEception(status_code=400,details=f"Item with {item.id} already exists.")
    if all(info is None for info in (name,price,count)):
        raise HTTPEception(status_code=400,details="No information to update.")
    item = items[item_id]
    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    if count is not None:
        item.count = count
    if category is not None:
        item.category = category

    return {"updated":item}

@app.get("/category/{category}")
def quuery_item_by_category(category:Category)->dict[str,Selection]:
    selection = [items for items in items.values() if item.category == category]
    return {
            "query": {"category":category},
        "selection":selection
    }:



