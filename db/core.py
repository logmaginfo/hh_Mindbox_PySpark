import csv
from db.models import sync_session, Products_Child, Categories_Parent, Base, sync_engine
from sqlalchemy import text

# наполняем базу
def cat_prod_add():
    with sync_session() as session:#fihin
        l = []
        c1 = Categories_Parent(name_cat="Овощи-фрукты")
        p1 = Products_Child(name_pr="Бананы")
        c1.product.append(p1)
        l.append(c1)
        l.append(p1)
        c2 = Categories_Parent(name_cat="Кондитерские изделия")
        p2 = Products_Child(name_pr="Печенье")
        c2.product.append(p2)
        l.append(c2)
        l.append(p2)
        c3 = Categories_Parent(name_cat="Мясная продукция")
        p3 = Products_Child(name_pr="Колбаса")
        c3.product.append(p3)
        l.append(c3)
        l.append(p3)
        c4 = Categories_Parent(name_cat="Молочная продукция")
        p4 = Products_Child(name_pr="Молоко")
        c4.product.append(p4)
        l.append(c4)
        l.append(p4)
        c5 = Categories_Parent(name_cat="Спиртное")
        l.append(c5)
        p5= Products_Child(name_pr="Сметана")
        c4.product.append(p5)
        p6 = Products_Child(name_pr="Энергетик")
        l.append(p5)
        l.append(p6)
        session.add_all(l)
        session.commit()

# def для соз-я ф-а csv
def csv_f(name:str, title:tuple, items:tuple):
    with open(name, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(title)
        for row in items:
            writer.writerow(row)

# соз-ем ф-ы csv
def get_df():
    with sync_session() as session:
        pr = session.execute(text("SELECT id, name_pr FROM products"))
        csv_f("prod.csv", ("prod_id","name_prod"), pr.all())
        pr = session.execute(text("SELECT id, name_cat FROM categories"))
        csv_f("cat.csv", ("cat_id","name_cat"), pr.all())
        pr = session.execute(text("SELECT cat_id, prod_id FROM association_table_cat_prod"))
        csv_f("prod_cat.csv", ("cat_id","prod_id"), pr.all())

def create_table():
    Base.metadata.create_all(sync_engine)

create_table()
get_df()