from fastapi import FastAPI,Depends,HTTPException
from sqlmodel import SQLModel , Field, create_engine, Session,select
from product_service import setting
from typing import List
from contextlib import asynccontextmanager




class Product_service (SQLModel,table= True):
 id: int| None =Field(default=None,primary_key=True)
 product_id: int| None =Field(default=None)
 product_name:str= Field(index=True, min_length=3, max_length=54)
 product_price: int| None =Field(default=None)
 




# connection_string
connection_string:str= str(setting.DATABASE_URL).replace("postgresql","postgresql+psycopg")
engine=create_engine(connection_string,connect_args={"sslmode":"require"},pool_recycle=300,pool_size=10,echo=True)




#engine
def create_table():
   SQLModel.metadata.create_all(engine)


def get_session ():
    with Session(engine) as session:
      yield session

# todo1:Todo=Todo(content="task1")
# todo2:Todo=Todo(content="task2")
# #session
# session= Session(engine)
# session.add(todo1)
# session.add(todo2)
# print(  f'before commit{todo1}')
# session.commit()
# print  (f'after commit{todo1}')
# session.refresh(todo1)
# session.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
   print("creating table")
   create_table()
   print("table created")
   yield



app=FastAPI(lifespan=lifespan,title="Product service",version='1.0.0')


@app.get('/')
async def products():
    return{"message":"welcome to the Zia Mart product service"}





@app.post('/addproduct/',response_model=Product_service)
async def create_product(product:Product_service, session: Session= Depends(get_session)):
   session.add(product)
   session.commit()
   session.refresh(product)
   return product


@app.get('/getallproduct/',response_model=list[Product_service])
async def get_all(session:Session= Depends(get_session)):
     products=session.exec(select(Product_service)).all()
     return products


@app.get('/getsingleproduct/{product_id}',response_model=Product_service)
async def get_single_product(product_id:int,session:Session=Depends(get_session)):
   product=session.exec(select(Product_service).where(Product_service.product_id ==product_id)).first()
   if product:
      return product
   else:
      raise HTTPException(status_code=404,detail="no product found")
   



@app.put('/changeproduct/{product_id}')
async def edit_product(id:int ,product: Product_service, session:Session=Depends(get_session)):
   existing_product = session.exec(select(Product_service).where(Product_service.id == id)).first()
   if existing_product:
      existing_product.id== product.product_id
      existing_product.name ==product.product_name
      existing_product.price==product.product_price
      session.add(existing_product)
      session.commit()
      session.refresh(existing_product)
      return existing_product
   else:
      raise HTTPException(status_code=404,detail="no task found")
   


@app.delete('/poduct/{product_id}')
async def delete_product(id:int ,session:Session=Depends(get_session)):
   deleted_product=session.get(Product_service,id)
   if deleted_product:
      session.delete(deleted_product)
      session.commit()
      return {"message":"product successfully deleted"}
   else:
      raise HTTPException(status_code=404,detail="no product found")